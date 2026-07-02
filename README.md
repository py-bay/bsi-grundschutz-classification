# bsi-grundschutz-classification

Deduktive Prüfbarkeitsklassifikation der BSI-IT-Grundschutz-Anforderungen
(Schicht SYS, Edition 2023) in ein A/B/C-Schema: deterministisch prüfbar
(A) / kontext- und interpretationsabhängig (B) / normativ-organisatorisch
oder evidenzfrei (C). Das Repository enthält das Klassifikationsschema, die
menschliche Cross-Validation einer stratifizierten Stichprobe (n = 50) mit
Interkoderreliabilität und Adjudikation sowie die Auswahl der Träger für
die Lab-Evaluation der zugehörigen Bachelorarbeit.

Mittleres Glied einer Kette aus drei Repositories:

1. [bsi-grundschutz-parser](https://github.com/py-bay/bsi-grundschutz-parser)
   erzeugt die Datengrundlage aus den offiziellen BSI-PDFs.
2. **bsi-grundschutz-classification** (dieses Repository) klassifiziert
   die Anforderungen nach Prüfbarkeit und begründet die Auswahl der
   Lab-Träger.
3. [grundschutz-agent-lab](https://github.com/py-bay/grundschutz-agent-lab)
   führt die Lab-Evaluation durch: agentische Prüfung der ausgewählten
   B-Anforderungen gegen konstruierte Referenzzustände.

Die Klassifikation ist Vorarbeit, kein Endprodukt. Sie begründet, warum die
Lab-Evaluation auf Anforderungen der Kategorie B zielt. Sie misst keine
belastbare A/B/C-Verteilung des IT-Grundschutz. Der tragende Befund ist die
Lage der Uneinigkeit zwischen den Kodierern an der A/B- und der B/C-Grenze
(siehe Auswertung).

## Ablauf

Die Ordner unter `data/` folgen dem Ablauf der Klassifikation:

```
1_anforderungen → 2_schema → 3_kodierung → 4_adjudikation → 5_auswertung → 6_lab_auswahl
   Extraktion      A/B/C-      blind, 2      22 Diskrepanzen   ICR + Konsens    Träger fürs Lab
   (Parser)        Schema      Kodierer      besprochen        (Goldreferenz)   (Kategorie B)
```

### 1. Anforderungen (`data/1_anforderungen/`)

Eingefrorener Extraktionsstand aus
[bsi-grundschutz-parser](https://github.com/py-bay/bsi-grundschutz-parser):
die aktiven SYS-Anforderungen (`requirements.csv`) und ihre satzweise
Zerlegung (`sentences.csv`). Viele BSI-Anforderungen enthalten mehrere
normative Sätze — klassifiziert wird deshalb der einzelne Satz, die
vollständige Anforderung bleibt als Kontext erhalten. Spaltenbeschreibung
in `data/1_anforderungen/README.md`.

### 2. Schema (`data/2_schema/`)

Das deduktiv aus Forschungsfrage und Literatur abgeleitete A/B/C-Kodierschema
(`kodierschema.md`, Stand v2) mit Kodierregeln, Ankerbeispielen,
Entscheidungsbaum und der transparent dokumentierten Schema-Iteration
(Schärfung der B/C-Grenze am 2026-05-20, vor der Kodierung).

### 3. Kodierung (`data/3_kodierung/`)

Aus den Satz-Einheiten wurde eine stratifizierte Stichprobe gezogen —
n = 50, geschichtet nach Anforderungsstufe (Basis/Standard/erhöht),
deterministisch mit Seed 42:

- `stichprobe.csv` — die 50 gezogenen Satz-Einheiten mit Kontext
- `stichprobe_log.json` — Ziehungsmetadaten (Seed, Schichtung, Quelldatei)

Zwei Kodierer — der Autor und ein unabhängiger Zweitkodierer — kodierten
die 50 Sätze blind und unabhängig nach dem Schema
(Kodiervorlage: `coder_template.xlsx`):

- `coder_autor.csv`, `coder_zweitkodierer.csv` — die ausgefüllten
  Kodierbögen als anonymisierte Exporte (Rollen statt Namen; die
  XLSX-Originale verbleiben privat)

### 4. Adjudikation (`data/4_adjudikation/`)

Die 22 Diskrepanzen zwischen den Kodierern wurden in einer
Adjudikationsrunde (2026-05-27) besprochen:

- `adjudikation.csv` — je Diskrepanzfall beide Voten, Argumente, Konsens
  und Begründung. 19 Fälle wurden zu einem gemeinsamen Gold-Code
  konsentiert, 3 blieben als `needs_review` offen — alle drei an der A/B-
  oder B/C-Grenze.
- `schema_notizen.md` — die dabei festgehaltenen Schema-Beobachtungen
  (Ergebnis: keine weitere Schema-Iteration, das Schema blieb v2).

### 5. Auswertung (`data/5_auswertung/`)

Aus Kodierbögen und Adjudikation baut `scripts/build_human_consensus.py`
die Goldreferenz, `scripts/compute_icr.py` rechnet die
Interkoderreliabilität (Cohens Kappa paarweise, Fleiss Kappa, raw
agreement; methodisch nach McHugh 2012, Krippendorff 2018 und der
strukturierenden Inhaltsanalyse nach Kuckartz & Rädiker 2022):

- `konsens.csv` — Goldreferenz: `human_consensus` je Satz-Einheit
- `icr_full.txt` — Roh-Output beider ICR-Läufe (pre- und post-Adjudikation)

| Vergleich                        | n  | raw agreement | Cohens κ |
|----------------------------------|----|---------------|----------|
| Autor vs. Zweitkodierer (pre)    | 50 | 0,560         | 0,305    |
| Autor vs. Konsens (post)         | 47 | 0,723         | 0,547    |
| Zweitkodierer vs. Konsens (post) | 47 | 0,851         | 0,737    |

Fleiss' κ: 0,276 (pre, beide Kodierer), 0,533 (post, inkl. Konsens). Es
wird bewusst kein fester Kappa-Zielwert gesetzt: Die Klassifikation ist
Vorfilter für die Lab-Auswahl, nicht Endprodukt (Krippendorff 2018 bindet
die akzeptable Schwelle an die Konsequenzen). Der tragende Befund: Von den
22 Diskrepanzen liegen 16 (73 %) an einer der beiden B-Grenzen
(Autor=C/Zweitkodierer=B: n = 9; Autor=A/Zweitkodierer=B: n = 7). Die
Uneinigkeit konzentriert sich genau dort, wo die Lab-Evaluation ansetzt.

### 6. Lab-Auswahl (`data/6_lab_auswahl/`)

Kriteriengeleitete (purposive) Auswahl der B-Anforderungen als Träger für
die Lab-Evaluation in
[grundschutz-agent-lab](https://github.com/py-bay/grundschutz-agent-lab):
Auswahlprotokoll, Ergebnisklassen-Mapping mit Soll-Urteilen (Ground Truth)
und die Items maschinenlesbar. Details und das Verhältnis zum gewerteten
Hauptlauf der Arbeit in `data/6_lab_auswahl/README.md`.

## Reproduzierbarkeit

Benötigt wird nur [uv](https://docs.astral.sh/uv/) (Python 3.13 wird
automatisch verwaltet; die Skripte nutzen ausschließlich die
Standardbibliothek):

```bash
git clone https://github.com/py-bay/bsi-grundschutz-classification.git
cd bsi-grundschutz-classification

# Goldreferenz aus Kodierbögen + Adjudikation bauen
uv run python scripts/build_human_consensus.py

# Interkoderreliabilität pre-Adjudikation (n = 50)
uv run python scripts/compute_icr.py data/3_kodierung/coder_autor.csv data/3_kodierung/coder_zweitkodierer.csv

# Interkoderreliabilität post-Adjudikation gegen den Konsens (n = 47)
uv run python scripts/compute_icr.py data/3_kodierung/coder_autor.csv data/3_kodierung/coder_zweitkodierer.csv data/5_auswertung/konsens.csv
```

Die erwartete Ausgabe liegt eingefroren in `data/5_auswertung/icr_full.txt`;
`konsens.csv` wird von `build_human_consensus.py` identisch neu erzeugt.

Tests — verifizieren die Kappa-Berechnung gegen handgerechnete Beispiele
aus der Primärliteratur (Cohen 1960; Fleiss 1971; Scott 1955), die
Konsens-Regeln und die eingefrorenen Ergebnisse:

```bash
uv run python -m unittest discover tests
```

## Datenquelle

Die Anforderungstexte in `data/` stammen aus dem
[IT-Grundschutz-Kompendium, Edition 2023](https://www.bsi.bund.de/DE/Themen/Unternehmen-und-Organisationen/Standards-und-Zertifizierung/IT-Grundschutz/IT-Grundschutz-Kompendium/it-grundschutz-kompendium_node.html)
des Bundesamts für Sicherheit in der Informationstechnik (BSI) und
unterliegen dessen Nutzungsbedingungen.

## Lizenz

MIT (nur der Code — nicht die BSI-Inhalte, siehe Datenquelle).

