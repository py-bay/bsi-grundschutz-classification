"""Compute inter-coder reliability (ICR) for the A/B/C cross-validation.

Reads one or more filled coder files and reports:

  - per-pair raw agreement and Cohen's kappa (McHugh 2012),
  - confusion matrices,
  - Fleiss' kappa across all human coders (only when n_coders >= 2).

Usage:

    # Pre-Adjudikation (n = 50)
    uv run python scripts/compute_icr.py \
        data/3_kodierung/coder_autor.csv data/3_kodierung/coder_zweitkodierer.csv

    # Post-Adjudikation gegen den Konsens (needs_review ausgeschlossen, n = 47)
    uv run python scripts/compute_icr.py \
        data/3_kodierung/coder_autor.csv data/3_kodierung/coder_zweitkodierer.csv \
        data/5_auswertung/konsens.csv

Akzeptiert werden CSVs mit `unit_id` und einer Kategorien-Spalte
(`kategorie`, `classification` oder `human_consensus`). Der Output beider
Laeufe liegt eingefroren unter data/5_auswertung/icr_full.txt. Das Skript
nutzt ausschliesslich die Standardbibliothek.
"""

from __future__ import annotations

import argparse
import csv
import itertools
from collections import Counter
from pathlib import Path

CATS = ("A", "B", "C")


def _normalize(raw: str) -> str:
    """Map any coder value to a single-token category.

    Accepts plain ``A``/``B``/``C``/``unklar`` as well as the human-readable
    dropdown values (e.g. ``A — Deterministisch pruefbar``). Returns the
    leading letter for A/B/C, ``U`` for unklar/unknown variants, or ``""``
    if the cell is empty.
    """
    s = raw.strip()
    if not s:
        return ""
    if s.lower().startswith("needs"):
        return ""  # needs_review-Faelle werden vom Vergleich ausgeschlossen
    first = s[0].upper()
    if first in ("A", "B", "C"):
        return first
    if s.lower().startswith("unkl") or s.lower() in ("u", "?"):
        return "U"
    return first  # fall through unchanged; will show up in confusion matrix


def load_codes(path: Path, key: str = "kategorie") -> dict[str, str]:
    out: dict[str, str] = {}
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        # Fallback-Kette: kategorie (Kodierboegen) -> classification (legacy)
        # -> human_consensus (konsens.csv aus build_human_consensus.py).
        if reader.fieldnames and key not in reader.fieldnames:
            for cand in ("classification", "human_consensus"):
                if cand in reader.fieldnames:
                    key = cand
                    break
        for row in reader:
            uid = row["unit_id"]
            code = _normalize(row.get(key) or "")
            if code:
                out[uid] = code
    return out


def cohen_kappa(a: list[str], b: list[str]) -> tuple[float, float]:
    """Return (raw_agreement, Cohen's kappa) for two equally long label lists."""
    n = len(a)
    if n == 0:
        return 0.0, 0.0
    po = sum(1 for x, y in zip(a, b) if x == y) / n
    cats = sorted(set(a) | set(b))
    pe = 0.0
    ca = Counter(a)
    cb = Counter(b)
    for c in cats:
        pe += (ca[c] / n) * (cb[c] / n)
    if pe >= 1.0:
        return po, 1.0 if po == 1.0 else 0.0
    return po, (po - pe) / (1 - pe)


def fleiss_kappa(per_item: list[list[str]]) -> float:
    """Fleiss' kappa for >=2 raters; per_item[i] = labels by all raters on item i."""
    if not per_item:
        return 0.0
    n_raters = len(per_item[0])
    if n_raters < 2 or any(len(r) != n_raters for r in per_item):
        return 0.0
    cats = sorted({lab for r in per_item for lab in r})
    n = len(per_item)
    # P_j: marginal proportion of category j
    total_assignments = n * n_raters
    pj = {c: 0 for c in cats}
    for r in per_item:
        for lab in r:
            pj[lab] += 1
    pj = {c: pj[c] / total_assignments for c in cats}

    # P_i: extent of agreement on item i
    pi_vals: list[float] = []
    for r in per_item:
        cnt = Counter(r)
        s = sum(v * (v - 1) for v in cnt.values())
        pi_vals.append(s / (n_raters * (n_raters - 1)))

    p_bar = sum(pi_vals) / n
    pe = sum(v * v for v in pj.values())
    if pe >= 1.0:
        return 1.0 if p_bar == 1.0 else 0.0
    return (p_bar - pe) / (1 - pe)


def confusion(a: list[str], b: list[str], label_a: str, label_b: str) -> str:
    cats = sorted(set(a) | set(b))
    width = max(4, *(len(c) for c in cats))
    out = [f"\n  Konfusionsmatrix: {label_a} (Zeile) vs. {label_b} (Spalte)"]
    header = " " * (width + 2) + " ".join(f"{c:>{width}}" for c in cats)
    out.append(header)
    for ra in cats:
        row = [f"{ra:>{width}} |"]
        for rb in cats:
            n = sum(1 for x, y in zip(a, b) if x == ra and y == rb)
            row.append(f"{n:>{width}}")
        out.append(" ".join(row))
    return "\n".join(out)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("coder_files", nargs="+", type=Path,
                    help="filled coding_*.csv files (one per coder)")
    args = ap.parse_args()

    coders: dict[str, dict[str, str]] = {}
    for p in args.coder_files:
        name = p.stem
        for prefix in ("coder_", "coding_"):
            if name.startswith(prefix):
                name = name[len(prefix):]
                break
        coders[name] = load_codes(p)

    # Restrict to units coded by every coder.
    ids = sorted(set.intersection(*(set(c) for c in coders.values())))
    if not ids:
        raise SystemExit("Keine gemeinsam codierten Units zwischen den Codierern.")

    print(f"Verglichen werden {len(ids)} units; Codierer: {', '.join(coders)}")

    # Pairwise human vs. human
    for a, b in itertools.combinations(coders.keys(), 2):
        la = [coders[a][i] for i in ids]
        lb = [coders[b][i] for i in ids]
        po, k = cohen_kappa(la, lb)
        print(f"\n[{a} vs. {b}]  raw agreement = {po:.3f}   Cohen's kappa = {k:.3f}")
        print(confusion(la, lb, a, b))

    # Fleiss' kappa across humans (if >=2)
    if len(coders) >= 2:
        per_item = [[coders[c][i] for c in coders] for i in ids]
        fk = fleiss_kappa(per_item)
        print(f"\n[Fleiss' kappa, {len(coders)} Codierer]  kappa = {fk:.3f}")


if __name__ == "__main__":
    main()
