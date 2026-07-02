# Lab-Stichprobe: Träger-Auswahl für die Lab-Evaluation

Dieser Ordner dokumentiert, welche SYS-Anforderungen als Träger für die
Lab-Evaluation der zugehörigen Bachelorarbeit ausgewählt wurden und warum.
Die Auswahl ist kriteriengeleitet (purposive) mit dem Ziel, die fünf
Ergebnisklassen einer agentischen Prüfung abzudecken — sie ist keine
repräsentative Stichprobe und erlaubt keine Verteilungsaussage über den
IT-Grundschutz. Prüfeinheit ist der einzelne als B klassifizierte Satz im
Verbund mit einem konstruierten Referenzzustand, nicht die Anforderung als
Ganzes.

Die Lab-Evaluation selbst (Harness, Referenzzustände, Läufe, Auswertung)
liegt im Repository
[grundschutz-agent-lab](https://github.com/py-bay/grundschutz-agent-lab).

## Dateien

- `selection_log.json` — Auswahlprotokoll: Kandidatenraum,
  Machbarkeitsfilter, Kuration je Item, Pilot-Befunde und die
  v1→v2-Ersetzungen
- `ergebnisklassen_mapping.md` — Mapping der acht Items auf die fünf
  Ergebnisklassen mit Begründung, Soll-Urteil und Evidenz-Skizze
- `lab_requirements.csv` — dieselben acht Items maschinenlesbar (eine
  Zeile je Item)

## Verhältnis zum Hauptlauf der Arbeit

Die Dateien sind der eingefrorene Stand der Auswahl vor dem Hauptlauf
(v2 „container-treu", 2026-06-16). Der gewertete Hauptlauf besetzt die
fünf Ergebnisklassen mit den Items 1–4, 6 und 7: vier distinkte
Anforderungen (SYS.2.1.A18, SYS.1.1.A2, SYS.1.1.A33, SYS.1.1.A39) in fünf
Operationalisierungen, je ein adversariales Variantenpaar, also zehn
Prüffälle mit k = 4 Wiederholungen. Die Items 5 (SYS.2.3.A1) und 8
(SYS.1.1.A19) liegen außerhalb des gewerteten Hauptsatzes; sie dienen in
der Diskussion der Arbeit als fehlerinduzierende Grenzfälle.

Diese Auswahl ist methodisch von der Cross-Validation
(`../3_kodierung/` bis `../5_auswertung/`) getrennt: Die Cross-Validation
misst die Konsistenz der Klassifikationsentscheidung zwischen unabhängigen
Kodierern, die Lab-Auswahl bestimmt Träger für die Labor-Evaluation des
Prüfagenten. Eine Überlappung in Unit-IDs ist möglich, aber für die
Validität unerheblich.
