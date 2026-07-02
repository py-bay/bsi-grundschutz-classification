"""Build the human consensus gold-reference for the A/B/C cross-validation.

Liest die anonymisierten Kodierboegen (``data/3_kodierung/coder_*.csv``),
die Adjudikation (``data/4_adjudikation/adjudikation.csv``) und die
gezogene Stichprobe (``data/3_kodierung/stichprobe.csv``) und schreibt die
Goldreferenz nach ``data/5_auswertung/konsens.csv``.

Konsens je unit_id:

  - beide Kodierer vergaben denselben A/B/C-Code → dieser Code
    (``human_consensus_source = agreement``)
  - Diskrepanz, Adjudikation hat einen Konsens A/B/C → dieser Code
    (``human_consensus_source = adjudication``)
  - Diskrepanz, Adjudikation endete mit ``needs_review`` → der literale
    String ``needs_review`` (``human_consensus_source = adjudication``)
  - alle anderen Faelle → leere Zelle mit
    ``human_consensus_source = missing`` und einer Notiz

Usage:

    uv run python scripts/build_human_consensus.py

Das Skript nutzt ausschliesslich die Standardbibliothek.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_coder(path: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    with path.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            uid = (row.get("unit_id") or "").strip()
            code = (row.get("kategorie") or "").strip()
            if uid and code:
                out[uid] = code[0].upper()
    if not out:
        raise SystemExit(f"Keine Kodierungen (unit_id + kategorie) in {path}")
    return out


def load_adjudication(path: Path) -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    with path.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            uid = (row.get("unit_id") or "").strip()
            if not uid:
                continue
            out[uid] = {
                "konsens": (row.get("konsens") or "").strip(),
                "begruendung": (row.get("konsens_begruendung") or "").strip(),
            }
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=ROOT,
                    help="Repository-Wurzel (Default: relativ zum Skript)")
    args = ap.parse_args()
    root: Path = args.root

    master_p = root / "data/3_kodierung/stichprobe.csv"
    autor = load_coder(root / "data/3_kodierung/coder_autor.csv")
    zweitkodierer = load_coder(root / "data/3_kodierung/coder_zweitkodierer.csv")
    adj = load_adjudication(root / "data/4_adjudikation/adjudikation.csv")

    with master_p.open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
        fieldnames = list(rows[0].keys())

    extra = ["human_consensus", "human_consensus_source", "human_consensus_note"]
    out_fields = fieldnames + extra

    n_agreed = n_adj = n_needs_review = n_missing = 0
    for row in rows:
        uid = row["unit_id"]
        s = autor.get(uid, "")
        i = zweitkodierer.get(uid, "")
        if uid in adj:
            kon = adj[uid]["konsens"]
            if kon.lower() == "needs_review":
                row["human_consensus"] = "needs_review"
                row["human_consensus_source"] = "adjudication"
                row["human_consensus_note"] = adj[uid]["begruendung"]
                n_needs_review += 1
            elif kon in ("A", "B", "C"):
                row["human_consensus"] = kon
                row["human_consensus_source"] = "adjudication"
                row["human_consensus_note"] = adj[uid]["begruendung"]
                n_adj += 1
            else:
                row["human_consensus"] = ""
                row["human_consensus_source"] = "missing"
                row["human_consensus_note"] = f"adj-row found but konsens leer: '{kon}'"
                n_missing += 1
        elif s and i and s == i:
            row["human_consensus"] = s
            row["human_consensus_source"] = "agreement"
            row["human_consensus_note"] = ""
            n_agreed += 1
        else:
            row["human_consensus"] = ""
            row["human_consensus_source"] = "missing"
            row["human_consensus_note"] = f"autor={s} zweitkodierer={i} (no adjudication entry)"
            n_missing += 1

    out_p = root / "data/5_auswertung/konsens.csv"
    out_p.parent.mkdir(parents=True, exist_ok=True)
    with out_p.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=out_fields)
        w.writeheader()
        w.writerows(rows)
    print(f"Wrote {out_p}: agreed={n_agreed} adjudicated={n_adj} needs_review={n_needs_review} missing={n_missing}")


if __name__ == "__main__":
    main()
