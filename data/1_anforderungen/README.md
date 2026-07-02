# Anforderungen und Satz-Einheiten (Schicht SYS)

Eingefrorener Extraktionsstand aus
[bsi-grundschutz-parser](https://github.com/py-bay/bsi-grundschutz-parser),
Edition 2023:

- `requirements.csv` — die aktiven SYS-Anforderungen
- `sentences.csv` — die satzweise Zerlegung: Da viele BSI-Anforderungen
  mehrere normative Saetze enthalten, wird jeder Satz als eigene Einheit
  gefuehrt. Diese Satz-Einheiten sind die Klassifikationseinheiten des
  Schemas (`../2_schema/kodierschema.md`) und die Ziehungsgrundlage der
  Kodier-Stichprobe (`../3_kodierung/stichprobe_log.json` → `source_csv`).

Beide Dateien enthalten reine Extraktionsdaten. Die A/B/C-Klassifikation
selbst liegt nicht hier, sondern in `../3_kodierung/` bis
`../5_auswertung/`.

## Spalten (`sentences.csv`)

- `unit_id`: stabile Satz-ID, z. B. `SYS.1.1.A1.S01`.
- `requirement_id`: urspruengliche BSI-Anforderung.
- `sentence_index`: Position des Satzes innerhalb der Anforderung.
- `module_id`, `module_name`, `title`: Baustein-Zuordnung der Anforderung.
- `level`, `level_label`: Schutzbedarfsstufe (B/S/H).
- `roles`: zustaendige Rollen laut Baustein, sofern angegeben.
- `is_deprecated`: entfallene Anforderung — in dieser Datei durchgaengig `False`, da entfallene Anforderungen bei der Extraktion ausgeschlossen wurden.
- `sentence_text`: der einzelne Satz (Klassifikationseinheit).
- `requirement_text`: vollstaendige Anforderung als Kontext.
