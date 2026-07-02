"""Tests fuer scripts/build_human_consensus.py.

Geprueft werden die vier Konsens-Regeln (vgl. Docstring des Skripts und
README, Abschnitt Adjudikation) an einem synthetischen Minimalfall sowie
die exakte Regenerierbarkeit der eingecheckten Goldreferenz
data/5_auswertung/konsens.csv aus den eingecheckten Eingaben.

Methodischer Hintergrund der Konsens-Bildung (Diskrepanzen werden
diskursiv adjudiziert, ungeklaerte Faelle bleiben als needs_review
ausgewiesen): Kuckartz, U. & Raediker, S. (2022). Qualitative
Inhaltsanalyse: Methoden, Praxis, Computerunterstuetzung (5. Aufl.),
Kap. zur intersubjektiven Uebereinstimmung; zur Behandlung von
Uneinigkeit als Befund statt Messmangel: Krippendorff, K. (2018).
Content Analysis (4. Aufl.), Kap. 12.

Ausfuehren: uv run python -m unittest discover tests
"""

from __future__ import annotations

import csv
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

import build_human_consensus as bhc  # noqa: E402


def _write(path: Path, header: list[str], rows: list[list[str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


def _run_main(root: Path) -> list[dict[str, str]]:
    with mock.patch.object(sys, "argv", ["build_human_consensus.py", "--root", str(root)]):
        bhc.main()
    with (root / "data/5_auswertung/konsens.csv").open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


class TestKonsensRegeln(unittest.TestCase):
    """Die vier Regeln: agreement, adjudication, needs_review, missing."""

    def setUp(self) -> None:
        self._td = tempfile.TemporaryDirectory()
        self.root = Path(self._td.name)
        _write(
            self.root / "data/3_kodierung/stichprobe.csv",
            ["unit_id", "sentence_text"],
            [["u1", "Satz 1"], ["u2", "Satz 2"], ["u3", "Satz 3"], ["u4", "Satz 4"]],
        )
        _write(
            self.root / "data/3_kodierung/coder_autor.csv",
            ["unit_id", "kategorie"],
            [["u1", "A — Deterministisch pruefbar"], ["u2", "B"], ["u3", "A"], ["u4", "B"]],
        )
        _write(
            self.root / "data/3_kodierung/coder_zweitkodierer.csv",
            ["unit_id", "kategorie"],
            [["u1", "A"], ["u2", "C"], ["u3", "B"], ["u4", "C"]],
        )
        # u2 adjudiziert, u3 needs_review, u4 fehlt (-> missing).
        _write(
            self.root / "data/4_adjudikation/adjudikation.csv",
            ["unit_id", "konsens", "konsens_begruendung"],
            [["u2", "C", "Konservativregel."], ["u3", "needs_review", ""]],
        )

    def tearDown(self) -> None:
        self._td.cleanup()

    def test_konsensbildung(self) -> None:
        rows = {r["unit_id"]: r for r in _run_main(self.root)}

        # Regel 1: Uebereinstimmung beider Kodierer -> gemeinsamer Code.
        # (Dropdown-Langform "A — ..." wird auf "A" normalisiert.)
        self.assertEqual(rows["u1"]["human_consensus"], "A")
        self.assertEqual(rows["u1"]["human_consensus_source"], "agreement")

        # Regel 2: Diskrepanz mit Adjudikations-Konsens -> Gold-Code + Begruendung.
        self.assertEqual(rows["u2"]["human_consensus"], "C")
        self.assertEqual(rows["u2"]["human_consensus_source"], "adjudication")
        self.assertEqual(rows["u2"]["human_consensus_note"], "Konservativregel.")

        # Regel 3: Adjudikation ohne Konsens -> literales needs_review.
        self.assertEqual(rows["u3"]["human_consensus"], "needs_review")
        self.assertEqual(rows["u3"]["human_consensus_source"], "adjudication")

        # Regel 4: Diskrepanz ohne Adjudikations-Eintrag -> leer + Notiz.
        self.assertEqual(rows["u4"]["human_consensus"], "")
        self.assertEqual(rows["u4"]["human_consensus_source"], "missing")
        self.assertEqual(
            rows["u4"]["human_consensus_note"],
            "autor=B zweitkodierer=C (no adjudication entry)",
        )

    def test_spalten_der_stichprobe_bleiben_erhalten(self) -> None:
        rows = _run_main(self.root)
        self.assertEqual(
            list(rows[0].keys()),
            ["unit_id", "sentence_text",
             "human_consensus", "human_consensus_source", "human_consensus_note"],
        )
        self.assertEqual(rows[0]["sentence_text"], "Satz 1")


class TestRegenerierbarkeitGoldreferenz(unittest.TestCase):
    """konsens.csv laesst sich aus den eingecheckten Eingaben exakt neu bauen."""

    def test_konsens_csv_byte_identisch(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            for rel in (
                "data/3_kodierung/stichprobe.csv",
                "data/3_kodierung/coder_autor.csv",
                "data/3_kodierung/coder_zweitkodierer.csv",
                "data/4_adjudikation/adjudikation.csv",
            ):
                dst = root / rel
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy(REPO / rel, dst)
            (root / "data/5_auswertung").mkdir()

            _run_main(root)

            neu = (root / "data/5_auswertung/konsens.csv").read_text(encoding="utf-8")
            eingecheckt = (REPO / "data/5_auswertung/konsens.csv").read_text(encoding="utf-8")
            self.assertEqual(neu, eingecheckt)

    def test_zaehlung_wie_dokumentiert(self) -> None:
        # README/Anhang B: 28 Uebereinstimmungen + 19 adjudizierte +
        # 3 needs_review = 50; keine missing-Faelle.
        with (REPO / "data/5_auswertung/konsens.csv").open(encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        self.assertEqual(len(rows), 50)
        quellen = [r["human_consensus_source"] for r in rows]
        self.assertEqual(quellen.count("agreement"), 28)
        self.assertEqual(quellen.count("adjudication"), 22)  # 19 Gold + 3 needs_review
        self.assertEqual(quellen.count("missing"), 0)
        self.assertEqual(
            sum(1 for r in rows if r["human_consensus"] == "needs_review"), 3
        )


if __name__ == "__main__":
    unittest.main()
