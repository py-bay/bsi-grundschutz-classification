"""Tests fuer scripts/compute_icr.py gegen die Literatur und die eingefrorenen Werte.

Die Kappa-Implementierung wird auf drei Ebenen geprueft:

1. Handgerechnete Beispiele direkt aus den Formeln der Primaerliteratur
   (jede Erwartung ist im Test Schritt fuer Schritt hergeleitet):

   - Cohen, J. (1960). A coefficient of agreement for nominal scales.
     Educational and Psychological Measurement, 20(1), 37-46.
     Definition: kappa = (p_o - p_e) / (1 - p_e), mit p_o = beobachtete
     Uebereinstimmung und p_e = sum_j (Randanteil Rater A_j * Randanteil
     Rater B_j) als Zufallserwartung.
   - Fleiss, J. L. (1971). Measuring nominal scale agreement among many
     raters. Psychological Bulletin, 76(5), 378-382.
     Definition: kappa = (P_quer - P_e) / (1 - P_e), mit
     P_i = sum_j n_ij (n_ij - 1) / (n (n - 1)) je Item und
     P_e = sum_j p_j^2 ueber die gepoolten Kategorienanteile p_j.
   - Scott, W. A. (1955). Reliability of content analysis: The case of
     nominal scale coding. Public Opinion Quarterly, 19(3), 321-325.
     Fuer zwei Rater faellt Fleiss' Kappa mit Scotts Pi zusammen
     (gepoolte statt rater-spezifische Randverteilungen) und weicht
     dann bewusst von Cohens Kappa ab (Fleiss 1971, S. 378).

2. Bekannte Grenzfaelle: perfekte Uebereinstimmung (kappa = 1), exakt
   zufaellige Uebereinstimmung (kappa = 0), maximale Nicht-Uebereinstimmung
   bei symmetrischen Raendern (kappa = -1); vgl. Cohen (1960) und die
   Einordnung bei McHugh, M. L. (2012). Interrater reliability: the kappa
   statistic. Biochemia Medica, 22(3), 276-282.
3. Regression gegen die eingefrorenen Ergebnisse dieses Repositories (data/5_auswertung/icr_full.txt; identisch berichtet in Anhang B der zugehoerigen Bachelorarbeit). Ausfuehren: uv run python -m unittest discover tests
"""

from __future__ import annotations

import csv
import sys
import tempfile
import unittest
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

import compute_icr as ci  # noqa: E402


class TestCohenKappa(unittest.TestCase):
    """cohen_kappa() gegen die Formel aus Cohen (1960)."""

    def test_perfekte_uebereinstimmung_ist_1(self) -> None:
        # Cohen (1960): p_o = 1 impliziert kappa = 1, unabhaengig von p_e.
        labels = ["A", "B", "C", "A"]
        po, k = ci.cohen_kappa(labels, list(labels))
        self.assertEqual(po, 1.0)
        self.assertAlmostEqual(k, 1.0)

    def test_zufallsniveau_ist_0(self) -> None:
        # Handrechnung: a = [A,A,B,B], b = [A,B,A,B].
        # p_o = 2/4 = 0.5 (Positionen 1 und 4 stimmen ueberein).
        # Raender: beide Rater A: 0.5, B: 0.5
        # -> p_e = 0.5*0.5 + 0.5*0.5 = 0.5 (Cohen 1960).
        # kappa = (0.5 - 0.5) / (1 - 0.5) = 0.
        po, k = ci.cohen_kappa(["A", "A", "B", "B"], ["A", "B", "A", "B"])
        self.assertAlmostEqual(po, 0.5)
        self.assertAlmostEqual(k, 0.0)

    def test_2x2_handbeispiel_kappa_0_4(self) -> None:
        # 2x2-Kontingenztafel (Aufbau wie bei McHugh 2012), Zeile = Rater 1,
        # Spalte = Rater 2, n = 50:
        #          J    N
        #   J  |  20    5
        #   N  |  10   15
        # p_o = (20 + 15) / 50 = 0.7
        # Raender: Rater 1: J = 25/50 = 0.5, N = 0.5
        #          Rater 2: J = 30/50 = 0.6, N = 0.4
        # p_e = 0.5*0.6 + 0.5*0.4 = 0.5   (Cohen 1960)
        # kappa = (0.7 - 0.5) / (1 - 0.5) = 0.4
        a = ["J"] * 25 + ["N"] * 25
        b = ["J"] * 20 + ["N"] * 5 + ["J"] * 10 + ["N"] * 15
        po, k = ci.cohen_kappa(a, b)
        self.assertAlmostEqual(po, 0.7)
        self.assertAlmostEqual(k, 0.4)

    def test_maximale_nichtuebereinstimmung_ist_minus_1(self) -> None:
        # a = [A,B], b = [B,A]: p_o = 0, symmetrische Raender (0.5/0.5)
        # -> p_e = 0.5, kappa = (0 - 0.5) / 0.5 = -1 (Minimum bei p_e = 0.5,
        # vgl. Cohen 1960 zur Untergrenze -p_e/(1-p_e)).
        po, k = ci.cohen_kappa(["A", "B"], ["B", "A"])
        self.assertAlmostEqual(po, 0.0)
        self.assertAlmostEqual(k, -1.0)


class TestFleissKappa(unittest.TestCase):
    """fleiss_kappa() gegen die Formeln aus Fleiss (1971)."""

    def test_zwei_rater_handbeispiel_7_15(self) -> None:
        # Items (je 2 Rater): (A,A), (A,B), (B,B), (B,B).
        # P_i je Item mit n = 2: sum_j n_ij(n_ij - 1) / (2*1)
        #   -> 1, 0, 1, 1;  P_quer = 3/4 = 0.75
        # Gepoolte Anteile (8 Urteile): p_A = 3/8, p_B = 5/8
        #   -> P_e = (3/8)^2 + (5/8)^2 = 34/64 = 0.53125   (Fleiss 1971)
        # kappa = (0.75 - 0.53125) / (1 - 0.53125) = 7/15 = 0.4667
        per_item = [["A", "A"], ["A", "B"], ["B", "B"], ["B", "B"]]
        self.assertAlmostEqual(ci.fleiss_kappa(per_item), 7 / 15)

    def test_zwei_rater_entspricht_scotts_pi_nicht_cohens_kappa(self) -> None:
        # Fleiss (1971, S. 378) verallgemeinert Scotts Pi (1955), nicht
        # Cohens Kappa: die Zufallserwartung nutzt gepoolte Raender.
        # Beispiel mit ungleichen Raendern: a = [A,A,A,B], b = [A,A,B,B].
        # Cohen: p_o = 0.75; p_e = 0.75*0.5 + 0.25*0.5 = 0.5 -> kappa = 0.5
        # Fleiss/Scott: gepoolt p_A = 5/8, p_B = 3/8
        #   -> P_e = 34/64 = 0.53125 -> kappa = (0.75 - 0.53125)/0.46875 = 7/15
        a = ["A", "A", "A", "B"]
        b = ["A", "A", "B", "B"]
        _, cohens = ci.cohen_kappa(a, b)
        fleiss = ci.fleiss_kappa([[x, y] for x, y in zip(a, b)])
        self.assertAlmostEqual(cohens, 0.5)
        self.assertAlmostEqual(fleiss, 7 / 15)
        self.assertLess(fleiss, cohens)

    def test_drei_rater_perfekt_ist_1(self) -> None:
        # P_i = 3*2/(3*2) = 1 je Item -> P_quer = 1;
        # P_e = 0.5^2 + 0.5^2 = 0.5 -> kappa = (1 - 0.5)/(1 - 0.5) = 1.
        self.assertAlmostEqual(ci.fleiss_kappa([["A"] * 3, ["B"] * 3]), 1.0)

    def test_nur_eine_kategorie_gibt_1_bei_voller_uebereinstimmung(self) -> None:
        # Degenerierter Fall p_e = 1 (nur eine Kategorie im Material):
        # die Implementierung gibt bei P_quer = 1 definitionsgemaess 1.0
        # zurueck statt 0/0 zu teilen.
        self.assertEqual(ci.fleiss_kappa([["A", "A"], ["A", "A"]]), 1.0)

    def test_guards_fuer_unbrauchbare_eingaben(self) -> None:
        self.assertEqual(ci.fleiss_kappa([]), 0.0)                     # leer
        self.assertEqual(ci.fleiss_kappa([["A"]]), 0.0)                # < 2 Rater
        self.assertEqual(ci.fleiss_kappa([["A", "B"], ["A"]]), 0.0)    # ungleich


class TestNormalizeUndLoadCodes(unittest.TestCase):
    """Einlese-Schicht: Dropdown-Werte, needs_review, Spalten-Fallback."""

    def test_normalize(self) -> None:
        self.assertEqual(ci._normalize("A — Deterministisch pruefbar"), "A")
        self.assertEqual(ci._normalize(" b "), "B")
        self.assertEqual(ci._normalize("C"), "C")
        self.assertEqual(ci._normalize("unklar"), "U")
        self.assertEqual(ci._normalize("?"), "U")
        self.assertEqual(ci._normalize(""), "")
        # needs_review wird vom Vergleich ausgeschlossen (-> n = 47 statt 50
        # im Post-Adjudikations-Lauf, vgl. README Auswertung).
        self.assertEqual(ci._normalize("needs_review"), "")

    def _write(self, path: Path, header: list[str], rows: list[list[str]]) -> None:
        with path.open("w", encoding="utf-8", newline="") as f:
            w = csv.writer(f)
            w.writerow(header)
            w.writerows(rows)

    def test_load_codes_spalten_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            self._write(tmp / "kat.csv", ["unit_id", "kategorie"], [["u1", "A"]])
            self._write(tmp / "cls.csv", ["unit_id", "classification"], [["u1", "B"]])
            self._write(
                tmp / "kon.csv",
                ["unit_id", "human_consensus"],
                [["u1", "C"], ["u2", "needs_review"], ["u3", ""]],
            )
            self.assertEqual(ci.load_codes(tmp / "kat.csv"), {"u1": "A"})
            self.assertEqual(ci.load_codes(tmp / "cls.csv"), {"u1": "B"})
            # needs_review- und leere Zeilen fallen raus:
            self.assertEqual(ci.load_codes(tmp / "kon.csv"), {"u1": "C"})


class TestRegressionEingefroreneErgebnisse(unittest.TestCase):
    """Reproduziert data/5_auswertung/icr_full.txt aus den Kodier-CSVs.

    Erwartungswerte identisch mit Anhang B der Arbeit: pre-Adjudikation
    raw agreement 0,560 / Cohens Kappa 0,305 / Fleiss 0,276 (n = 50);
    post-Adjudikation Autor vs. Konsens 0,723/0,547 und Zweitkodierer vs.
    Konsens 0,851/0,737, Fleiss 0,533 (n = 47).
    """

    @classmethod
    def setUpClass(cls) -> None:
        data = REPO / "data"
        cls.autor = ci.load_codes(data / "3_kodierung/coder_autor.csv")
        cls.zweit = ci.load_codes(data / "3_kodierung/coder_zweitkodierer.csv")
        cls.konsens = ci.load_codes(data / "5_auswertung/konsens.csv")

    def test_pre_adjudikation_n50(self) -> None:
        ids = sorted(set(self.autor) & set(self.zweit))
        self.assertEqual(len(ids), 50)
        la = [self.autor[i] for i in ids]
        lz = [self.zweit[i] for i in ids]
        po, k = ci.cohen_kappa(la, lz)
        self.assertEqual(round(po, 3), 0.560)
        self.assertEqual(round(k, 3), 0.305)
        fk = ci.fleiss_kappa([[a, z] for a, z in zip(la, lz)])
        self.assertEqual(round(fk, 3), 0.276)

    def test_klassenverteilung_wie_anhang_b(self) -> None:
        # Anhang B, Tabelle Klassenverteilung: Autor A=10/B=13/C=27,
        # Zweitkodierer A=4/B=26/C=20.
        self.assertEqual(Counter(self.autor.values()), {"A": 10, "B": 13, "C": 27})
        self.assertEqual(Counter(self.zweit.values()), {"A": 4, "B": 26, "C": 20})

    def test_tragender_befund_diskrepanzen_an_den_b_grenzen(self) -> None:
        # README/Anhang B: 22 Diskrepanzen, davon 16 (73 %) an den beiden
        # B-Grenzen (Autor=C/Zweitkodierer=B: 9; Autor=A/Zweitkodierer=B: 7).
        paare = [(self.autor[i], self.zweit[i]) for i in self.autor]
        diskrepanzen = [(a, z) for a, z in paare if a != z]
        self.assertEqual(len(diskrepanzen), 22)
        self.assertEqual(diskrepanzen.count(("C", "B")), 9)
        self.assertEqual(diskrepanzen.count(("A", "B")), 7)

    def test_post_adjudikation_n47(self) -> None:
        ids = sorted(set(self.autor) & set(self.zweit) & set(self.konsens))
        self.assertEqual(len(ids), 47)  # 3x needs_review ausgeschlossen
        la = [self.autor[i] for i in ids]
        lz = [self.zweit[i] for i in ids]
        lk = [self.konsens[i] for i in ids]
        po, k = ci.cohen_kappa(la, lk)
        self.assertEqual((round(po, 3), round(k, 3)), (0.723, 0.547))
        po, k = ci.cohen_kappa(lz, lk)
        self.assertEqual((round(po, 3), round(k, 3)), (0.851, 0.737))
        fk = ci.fleiss_kappa([[a, z, c] for a, z, c in zip(la, lz, lk)])
        self.assertEqual(round(fk, 3), 0.533)


if __name__ == "__main__":
    unittest.main()
