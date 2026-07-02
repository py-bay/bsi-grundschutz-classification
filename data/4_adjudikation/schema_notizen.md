# Schema-Notizen aus der Adjudikation (2026-05-27)

Sammlung der waehrend der Adjudikation festgehaltenen Schema-Schwachstellen
zur spaeteren Entscheidung, ob eine Schema-v2.1-Iteration angesetzt wird.
Keine Schemaaenderung erfolgt aus diesen Notizen ohne explizite Freigabe;
das Schema bleibt vorerst v2.

## Notiz 1 — Einmalige Entscheidungen

- Fall: `SYS.1.2.3.A2.S01` ("Wenn vom Funktionsumfang her ausreichend, MUSS
  die Server-Core-Variante installiert werden.")
- Voten: Autor=C, Zweitkodierer=B → Konsens=B.
- Notiz: "Einmalige Entscheidungen mit als C-Kriterium aufnehmen."
- Lesart: Der Autor argumentierte, dass die Installationsvariante eine einmalige
  organisatorische Entscheidung ist und deshalb C sein muesste. Konsens
  blieb B mit der Begruendung "kann auch im nachhinein geprueft werden"
  (Konfiguration des installierten Systems ist auslesbar).
- Schema-Implikation (offen): Soll das B/C-Kriterium um "Einmaligkeit der
  Entscheidung" erweitert werden? Aktuell entscheidet das Schema nach
  Pruefbarkeit aus auslesbarer Evidenz, nicht nach Entscheidungs-Zeitpunkt.
  Eine Aufnahme wuerde mehrere Pattern-1-Faelle nach C verschieben und das
  vorhandene v2-Designziel ("im Zweifel B") untergraben. Empfehlung:
  **keine Aufnahme**; die C-Tendenz des Autors ist nicht durch eine
  Schemaluecke motiviert, sondern durch eine fortgesetzte v1-Bauchregel.

## Notiz 2 — Human in the Loop fehlt im Schema

- Fall: `SYS.1.7.A27.S03` ("Bei der Uebertragung von Programm-Quellcode
  SOLLTE geprueft werden, ob alle Zeichen richtig uebersetzt wurden.")
- Voten: Autor=A, Zweitkodierer=C → Konsens=C.
- Notiz: Vorschlag einer vierstufigen Klassifikation
  - A) vollautomatisch
  - B) automatisch mit Kontext
  - C) mit Human in the Loop
  - D) nur Mensch
  - "Verantwortungen vielleicht mit aufnehmen"
- Lesart: Das Schema unterscheidet aktuell nur "technisch+eindeutig" (A),
  "technisch+kontextabhaengig" (B) und "organisatorischer Akt /
  evidenzfrei" (C). Die Achse "Wer fuehrt die Pruefung aus — Skript,
  Skript-mit-Mensch, Mensch?" ist tatsaechlich nicht orthogonal abgebildet.
- Schema-Implikation (offen): Eine vierte Kategorie waere ein Bruch mit
  dem Ablauf der bisherigen ICR (zweimal kodiert nach 3-Kategorien-Schema)
  und der Lab-Auswahl, die explizit auf B aufsetzt. **Wenn ueberhaupt,
  als Sub-Dimension in der Lab-Diskussion zu fuehren, nicht als
  Kategorienaenderung in der Klassifikation.**
- Alternative im aktuellen Schema: Faelle mit "Mensch fuehrt Pruefung
  zwingend aus" sind nach v2 schon korrekt als C zu kodieren ("verlangt
  einen organisatorischen Akt"). Die Trennlinie ist also weniger eine
  Schemaluecke als eine Ankerbeispiel-Luecke.

## Notiz 3 — Ausschluss von Verweisen auf andere Bausteine

- Fall: `SYS.2.6.A7.S01` ("Die Moeglichkeiten der VDI-Loesung SOLLTEN fuer
  die Haertung der virtuellen Clients entsprechend den Anforderungen des
  Bausteins SYS.2.5 Client-Virtualisierung genutzt werden.")
- Voten: Autor=B, Zweitkodierer=C → Konsens=C.
- Notiz: "Ausschluss von Verweisen"
- Lesart: Saetze, die ihren Sollwert ausschliesslich aus einem anderen
  Baustein des Grundschutzkompendiums beziehen, sind ohne Lektuere des
  Verweisziels nicht entscheidbar. Konservativregel hat hier C ergeben.
- Schema-Implikation (offen): Sollte die Stichprobenziehung Saetze mit
  reinen Verweisen ("entsprechend den Anforderungen des Bausteins XYZ")
  vorab ausschliessen oder explizit als eigenstaendige C-Kategorie
  ausweisen? Das beruehrt eher die **Stichprobenkonstruktion** (ein Filter
  bei der Ziehung) als das A/B/C-Schema selbst.
- Empfehlung: Bei der Lab-Auswahl explizit pruefen, ob Saetze mit reinen
  Verweisen ausgeschlossen werden sollten — siehe
  `../6_lab_auswahl/ergebnisklassen_mapping.md`.

## Zusammenfassung

Keine der drei Notizen rechtfertigt nach jetziger Sicht eine
Schema-v2.1-Iteration. Notiz 2 (Human-in-the-Loop-Achse) ist die
substantiellste Beobachtung und gehoert in die **Diskussion** des
Methodikkapitels — sie illustriert die nicht-orthogonale Natur der
A/B/C-Klassifikation und stuetzt die Lab-getragene Validierung.
Notizen 1 und 3 sind eher Codiererschulungs- bzw.
Stichprobenkonstruktionsthemen.

Ergebnis: Es wurde keine v2.1-Iteration angesetzt; das Schema blieb
unveraendert v2. Die Notizen bleiben als dokumentierte Beobachtungen aus
der Adjudikation stehen.
