# Klassifikationsschema fuer SYS-Anforderungen

Stand: 2026-05-20 (Schaerfung Kategorie C; siehe Abschnitt "Schema-Iteration").

## Ziel

Dieses Kodierschema dient dazu, aktive Anforderungen des BSI-IT-Grundschutz-Bausteins SYS nach ihrer strukturellen Automatisierbarkeit zu klassifizieren. Die Klassifikation beantwortet nicht, ob eine konkrete Implementierung bereits existiert, sondern ob die Anforderung nach ihrem Text und der benoetigten Evidenz prinzipiell automatisiert pruefbar ist.

## Methodische Einordnung

Die Kategorien werden deduktiv aus Forschungsfrage, Expose und Literatur abgeleitet. Die Kodierung folgt dem Prinzip einer strukturierenden Inhaltsanalyse: Das Material wird anhand vorab definierter Kategorien analysiert; Kodierregeln und Ankerbeispiele sollen die Nachvollziehbarkeit erhoehen.

Wichtige Literaturbezuge:

- `Mayring2015` und `Kuckartz2018`: strukturierende qualitative Inhaltsanalyse und Kodierlogik.
- `Amor2021`: Automated Compliance Checking setzt voraus, dass normative Anforderungen in computable rules oder pruefbare Modelle ueberfuehrt werden koennen.
- `Yanagawa2024`: Compliance-as-Code und Policy-as-Code beschreiben regelbasierte Validierung von Systemzustaenden gegen Sollvorgaben.
- `Xiao2012` und `Alohaly2019`: natuerlichsprachliche Security Policies koennen teilweise in maschinennahe Policy-Elemente ueberfuehrt werden, bleiben aber domänenspezifisch und kontextabhaengig.
- `Huang2025`: LLM-basierte Systeme bringen Risiken wie Halluzinationen und eingeschraenkte Nachvollziehbarkeit mit; KI-Pruefungen brauchen daher Evidenz, Begruendung und Grenzen.

## Klassifikationseinheit

Klassifiziert wird der einzelne Satz einer aktiven SYS-Anforderung. Die vollstaendige Anforderung bleibt als Kontext erhalten.

Begruendung:

- Viele BSI-Anforderungen enthalten mehrere normative Aussagen.
- Innerhalb einer Anforderung koennen Saetze unterschiedlich automatisierbar sein.
- Eine pauschale Klassifikation ganzer Anforderungen wuerde gemischte Anforderungen verdecken.

Beispiel:

- Anforderung: `SYS.1.1.A1`
- Satz-Einheit: `SYS.1.1.A1.S01`
- Satz-Einheit: `SYS.1.1.A1.S02`

## Kategorien

### Kategorie A: Deterministisch pruefbar / regelbasiert automatisierbar

Ein Satz wird als Kategorie A klassifiziert, wenn er durch eindeutig definierbare technische Evidenz und regelbasierte Auswertung geprueft werden kann **und der Sollwert eindeutig bestimmt ist**.

Typische Merkmale:

- Konkreter Systemzustand, Konfigurationswert, installierte Komponente, aktivierter Dienst oder Netzwerkregel.
- Messbare oder direkt abfragbare Eigenschaft.
- Pruefung kann durch Skript, Tool, Policy-as-Code, Query oder statische Regel erfolgen.
- Keine semantische Auslegung des Zwecks erforderlich, sobald Sollwert und Zielsystem bekannt sind.
- Der **Sollwert** ergibt sich entweder direkt aus dem Satz (z. B. "MUSS deaktiviert sein"), aus dem zugehoerigen Anforderungstext oder aus allgemein anerkannten technischen Standards. Ist der Sollwert nur ueber organisatorische Vorgaben festlegbar, ist der Satz nicht `A`.

Kodierregel:

Wenn die Pruefung als deterministische Funktion aus technischer Evidenz und Sollregel formulierbar ist und der Sollwert eindeutig bestimmt ist, kodiere `A`.

Ankerbeispiele:

| Unit | Satz | Begruendung |
|---|---|---|
| `SYS.1.1.A15.S01` | Jeder Server SOLLTE an eine unterbrechungsfreie Stromversorgung (USV) angeschlossen werden. | Der Zielzustand kann ueber Inventar, Monitoring oder Infrastruktur-Daten gegen Serverliste geprueft werden. |
| `SYS.4.4.A5.S03` | Die UPnP-Funktion MUSS an allen Routern deaktiviert sein. | Konkreter Konfigurationszustand, regelbasiert pruefbar, sofern Routerzugriff/Evidenz vorhanden ist. |

### Kategorie B: Kontext- oder interpretationsabhaengig / KI-gestuetzt pruefbar

Ein Satz wird als Kategorie B klassifiziert, wenn technische **oder dokumentarische** Evidenz benoetigt wird, die Bewertung aber semantische Interpretation, Infrastrukturkontext oder Abgleich mehrerer Informationsquellen erfordert — typischerweise, weil der **Sollwert nicht eindeutig im Satz steht** und erst aus dem Betriebskontext rekonstruiert werden muss.

Typische Merkmale:

- Begriffe wie geeignet, erforderlich, angemessen, relevante, nachvollziehbar, regelmaessig oder sicher kommen vor und muessen kontextualisiert werden.
- Die Anforderung ist technisch oder dokumentarisch gerichtet, aber der Sollzustand ist nicht vollstaendig im Satz kodiert.
- Die Pruefung benoetigt Systemkontext, Dokumentation, Architekturwissen oder organisatorische Vorgaben.
- Ein Agent kann Evidenz sammeln, interpretieren und begruenden; das Ergebnis sollte fuer Menschen nachvollziehbar bleiben.

**Bewertung von Dokumentation als B-Fall.** Saetze, die die Existenz, Vollstaendigkeit oder Qualitaet von Dokumentation pruefen (z. B. "nachvollziehbar dokumentiert", "vollstaendig dokumentiert"), fallen unter B, sofern die Dokumentation prinzipiell zugaenglich gemacht werden kann (Code-Repository, Wiki, Dokumentenmanagement, SharePoint via MCP-Adapter). Die Bewertung der Qualitaet ist genau die B-typische Interpretationsleistung. Nicht ergebnisrelevant ist, ob der konkrete Lab-Aufbau dieser Arbeit Zugriff auf die Dokumentation hat — das ist eine Lab-Limitation, keine Eigenschaft der Anforderung.

Abgrenzung A vs. B:

- `A`: Sollwert eindeutig bestimmt, Pruefung ist Vergleichsoperation.
- `B`: Sollwert kontextabhaengig zu rekonstruieren, Pruefung enthaelt eine Interpretationsentscheidung. Auch wenn alle Evidenz technisch verfuegbar ist, bleibt der Satz `B`, sofern die Auslegung eines Begriffs ergebnisrelevant ist.

Kodierregel:

Wenn technische oder dokumentarische Evidenz vorhanden oder erhebbar ist, aber die Bewertung eine Bruecke zwischen natuerlichem Anforderungstext und Kontextwissen erfordert, kodiere `B`.

Ankerbeispiele:

| Unit | Satz | Begruendung |
|---|---|---|
| `SYS.1.1.A23.S01` | Das Server-System SOLLTE in ein geeignetes Systemueberwachungs- oder Monitoringkonzept eingebunden werden. | Monitoring-Evidenz ist technisch pruefbar, aber "geeignetes Konzept" erfordert Kontext und Bewertung. |
| `SYS.1.1.A19.S01` | Vorhandene lokale Paketfilter SOLLTEN ueber ein Regelwerk so ausgestaltet werden, dass die eingehende und ausgehende Kommunikation auf die erforderlichen Kommunikationspartner, Kommunikationsprotokolle sowie Ports und Schnittstellen beschraenkt wird. | Paketfilter sind auslesbar, aber "erforderlich" benoetigt Wissen ueber Dienste, Kommunikationsbeziehungen und Betriebszweck. |
| `SYS.1.1.A1.S03` | Bei virtualisierten Servern MUSS der Zugriff auf die Ressourcen der Instanz und deren Konfiguration ebenfalls auf die berechtigten Personen begrenzt werden. | Zugriffsdaten sind technisch erhebbar, aber "berechtigte Personen" setzt Rollen-/Berechtigungskonzept voraus. |
| `SYS.1.1.A21.S01` | Betriebliche Aufgaben, die an einem Server durchgefuehrt werden, SOLLTEN nachvollziehbar dokumentiert werden (Wer?, Wann?, Was?). | Dokumentation ist prinzipiell auslesbar (z. B. Ticketsystem, Change-Log, Wiki); "nachvollziehbar" ist die ergebnisrelevante Interpretation. Frueher C, seit Schaerfung 2026-05-20 B. |

### Kategorie C: Organisatorischer Akt oder evidenzfreie Bewertung

Ein Satz wird als Kategorie C klassifiziert, wenn die Pruefung einen **organisatorischen Akt** verlangt (Freigabe, Benennung, Beschluss, Sensibilisierung) oder **systematisch evidenzfrei** ist — also auch mit beliebig gutem Datenzugang kein Pruefurteil aus Evidenz ableitbar waere.

Typische Merkmale:

- Fokus auf Akte: Genehmigung, Freigabe, Benennung, Beauftragung, Inkraftsetzung, Schulung, Sensibilisierung.
- Die Wirksamkeit oder Angemessenheit der Massnahme ist nicht aus Artefakten ableitbar, sondern setzt eine Bewertung voraus, die nur durch einen Menschen vor Ort getroffen werden kann (z. B. "Verstehen die Mitarbeitenden die Schulungsinhalte?").
- Auch ein Agent mit Vollzugriff auf alle Dokumente und Systeme koennte das Urteil nicht valide faellen.

Abgrenzung B vs. C (zentrale Schaerfung 2026-05-20):

- `B`: Es existiert prinzipiell pruefbare Evidenz (technisch oder dokumentarisch), die Schwierigkeit liegt in der **Interpretation** der Evidenz. Das schliesst Bewertung von Dokumentationsqualitaet, Vollstaendigkeit und Nachvollziehbarkeit ein.
- `C`: Es existiert keine pruefbare Evidenz, oder die Pruefung ist der organisatorische Akt selbst.

Kodierregel:

Wenn die Erfuellung der Anforderung einen organisatorischen Akt voraussetzt oder kein Pruefurteil aus Evidenz ableitbar waere, kodiere `C`. Wenn Evidenz prinzipiell existiert und nur die Bewertung schwierig ist, kodiere `B`.

Ankerbeispiele:

| Unit | Satz | Begruendung |
|---|---|---|
| `SYS.1.1.A11.S01` | Ausgehend von der allgemeinen Sicherheitsrichtlinie der Institution SOLLTEN die Anforderungen an Server in einer separaten Sicherheitsrichtlinie konkretisiert werden. | Wirkt wie B (Richtlinie auslesbar), ist aber C, weil die Anforderung den **Akt der Konkretisierung durch die Institution** verlangt — nicht nur die Existenz eines Dokuments. |
| `SYS.1.1.A22.S02` | Dazu SOLLTEN die Notfallanforderungen an den Server ermittelt und geeignete Notfallmassnahmen umgesetzt werden, z. B. indem Wiederanlaufplaene erstellt oder Passwoerter und kryptografische Schluessel sicher hinterlegt werden. | Notfallanforderungen muessen organisatorisch ermittelt und institutionell beschlossen werden; "geeignet" ist hier ein Angemessenheitsurteil ohne ableitbare Evidenz. |
| `SYS.3.3.A3.S01` | Mitarbeitende MUESSEN fuer die besonderen Gefaehrdungen der Informationssicherheit durch Mobiltelefone sensibilisiert werden. | Sensibilisierung ist ein paradigmatischer organisatorischer Akt: Die Anforderung *ist* der Akt selbst (Mitarbeitende sensibilisieren), nicht die Existenz oder Bewertung eines Dokuments. Abgrenzung zu B: Es gibt kein inhaltstragendes Artefakt, dessen Pruefung die Anforderung erfuellen wuerde — der Akt selbst ist die Anforderung. |

Negative Abgrenzung (frueher C, jetzt B):

- `SYS.1.1.A21.S01` (Dokumentation Wer/Wann/Was) — jetzt B, weil Dokumentation auslesbar und die Bewertung von "nachvollziehbar" eine Interpretationsleistung ist.

## Entscheidungsbaum

1. Ist der Satz entfallen oder rein redaktionell?
   - Nicht klassifizieren beziehungsweise aus der Stichprobe ausschliessen.
2. Bezieht sich der Satz auf einen konkreten technischen Zustand, der direkt abgefragt oder regelbasiert verglichen werden kann?
   - Ja: Kategorie A, sofern keine wesentliche Kontextbewertung noetig ist.
3. Bezieht sich der Satz auf einen technischen Zustand, aber mit unklarem Sollwert, Kontextbegriff oder semantischem Abgleich?
   - Ja: Kategorie B.
4. Bezieht sich der Satz auf einen **organisatorischen Akt** (Freigabe, Benennung, Beschluss, Sensibilisierung) ODER waere auch mit beliebigem Datenzugang **kein Pruefurteil aus Evidenz** ableitbar?
   - Ja: Kategorie C.
   - Nein, aber die Pruefung verlangt Bewertung von Dokumentationsqualitaet, Vollstaendigkeit oder Nachvollziehbarkeit, wobei die Dokumentation prinzipiell zugaenglich gemacht werden kann: Kategorie B.
5. Bleibt der Fall unklar?
   - Kontext der vollstaendigen Anforderung pruefen und in `rationale` begruenden. Bei gleicher Plausibilitaet die konservativere Kategorie waehlen: `C` vor `B`, `B` vor `A`.

## Umgang mit Grenzfaellen

- Wenn ein Satz technische Evidenz und organisatorische Bewertung kombiniert, wird die fuer die valide Entscheidung notwendige hoechste Kategorie gewaehlt.
- Wenn die technische Pruefung nur eine Vorpruefung liefert, die finale Bewertung aber Kontext braucht, wird `B` oder `C` gewaehlt.
- Wenn ein Begriff wie "geeignet" oder "angemessen" durch eine externe, explizite Regel eindeutig operationalisiert ist, kann der Satz fuer diese konkrete Operationalisierung `A` sein. Ohne solche Regel bleibt er `B` oder `C`.
- Wenn ein Satz eine Liste mehrerer Teilanforderungen enthaelt, wird er nur dann als `A` klassifiziert, wenn alle Teilanforderungen deterministisch pruefbar sind. Andernfalls wird die hoechste erforderliche Kategorie gewaehlt.
- Ein Beispiel fuer einen technischen Grenzfall ist `SYS.1.1.A19.S01` (lokale Paketfilter). Existenz und Regelwerk sind auslesbar, aber "erforderliche Kommunikationspartner" benoetigt Kontextwissen. Nach Konservativregel wird er als `B` klassifiziert.

## Bewusste Einschraenkungen des Schemas

Das Schema ist drei-stufig (A/B/C) und bewusst grob. Es trifft keine
Aussage darueber, ob ein als `B` eingestufter Satz von einem konkreten
agentischen Pruefsystem im Lab korrekt geprueft werden koennte. Insbesondere:

- **Physische Welt.** Manche SYS-Anforderungen verlangen physische
  Pruefung (z. B. Sichtkontrolle in Serverraeumen, Inspektion von
  Hardwaresiegeln). Solche Saetze koennen technisch `B` sein —
  Evidenz waere prinzipiell sammelbar —, sind aber durch das in
  dieser Arbeit eingesetzte rein virtuelle Lab nicht abdeckbar.
  Die Klassifikation bewertet die *prinzipielle* Pruefbarkeit; die
  Lab-Evaluation bewertet, was unter den konkreten Lab-Bedingungen
  pruefbar ist. Die Trennung ist im Methodikkapitel als
  Validitaetsperimeter dokumentiert.
- **Keine feinere Granularitaet innerhalb B.** Innerhalb der
  B-Klasse wird nicht weiter unterschieden (z. B. nach Schwierigkeit
  der Auslegung). Solche Differenzierungen waeren mit n = 50
  Cross-Validation-Items nicht reliabel messbar.
- **Konservativregel als Bias.** Die Wahl "C ≻ B ≻ A" im Zweifel
  ist risikoavers und kann die A-Quote unterzeichnen. Diese
  Entscheidung wird in der Methodik ausdruecklich als Bias-Quelle
  ausgewiesen.

## Aggregation auf Anforderungsebene

Die finale Kodierung erfolgt auf Satzebene. Fuer Ergebnisdarstellungen auf Anforderungsebene wird eine aggregierte Kategorie abgeleitet:

- `A`: Alle Saetze der Anforderung sind `A`.
- `B`: Mindestens ein Satz ist `B`, kein Satz ist `C`.
- `C`: Mindestens ein Satz ist `C`.
- `mixed`: Optionaler Analysehinweis, wenn eine Anforderung Saetze aus mehreren Kategorien enthaelt.

Begruendung:

Eine Anforderung ist nur dann vollstaendig regelbasiert automatisierbar, wenn alle ihre relevanten Saetze regelbasiert automatisierbar sind. Sobald ein Satz menschliche Entscheidung verlangt, bleibt die Gesamtanforderung nicht vollautomatisierbar.

## Kodierfelder

Die Klassifikationsdatei soll mindestens folgende Felder enthalten:

- `unit_id`
- `requirement_id`
- `sentence_text`
- `classification`: `A`, `B` oder `C`
- `classification_label`
- `rationale`
- `evidence_needed`
- `coder`
- `review_status`

## Review-Regeln

- Jede Klassifikation braucht eine kurze Begruendung in `rationale`.
- `evidence_needed` beschreibt, welche Evidenz fuer eine valide Pruefung benoetigt wuerde.
- Unsichere Faelle erhalten `review_status = needs_review`.
- Fuer Inter-Coder-Reliabilitaet wird eine Teilmenge unabhaengig zweitkodiert.

## Schema-Iteration

Das Schema wurde zwischen erstem Klassifikationsdurchlauf und Inter-Coder-Reliabilitaet einmal geschaerft. Eine solche Iteration ist in der strukturierenden Inhaltsanalyse vorgesehen (Mayring 2015, Kuckartz & Raediker 2022) und wird hier transparent dokumentiert.

**Aenderung 2026-05-20.** Trennlinie B/C geschaerft: Kategorie C ist seither auf **organisatorische Akte** und **systematisch evidenzfreie Bewertungen** beschraenkt. Bewertung von Dokumentationsqualitaet, Vollstaendigkeit und Nachvollziehbarkeit faellt unter B, weil ein KI-Agent diese prinzipiell durchfuehren kann, sobald die Dokumentation zugaenglich gemacht wird (Code-Repository, Wiki, Dokumentenmanagement, SharePoint via MCP-Adapter). Die Lab-Limitation "Welche Dokumentenquellen sind im konkreten Lab-Aufbau verfuegbar?" wird auf der Lab-Ebene diskutiert, nicht in der Klassifikation.

Anlass der Aenderung: Beim Sichtungsdurchgang fiel auf, dass das ursprueliche C-Ankerbeispiel `SYS.1.1.A21.S01` ("Betriebliche Aufgaben SOLLTEN nachvollziehbar dokumentiert werden") nach der Logik des Schemas eigentlich B war — die Bewertung der Nachvollziehbarkeit ist genau die B-typische Interpretationsleistung. Die Schaerfung beseitigt diese Inkonsistenz und verschiebt erwartbar einen Teil der bisherigen C-Saetze nach B.

**Konsequenz.** Das Cross-Validation-Sample (`../3_kodierung/`) wurde nach
dem geschaerften Schema neu gezogen. Bereits begonnene menschliche Kodierungen
sind nach altem Schema entstanden und wurden vor der ICR-Auswertung neu gemacht.

Begruendungslogik fuer das Methodikkapitel: Die Iteration folgt der Mayring-Empfehlung, das deduktive Schema nach erstem Material-Durchgang zu pruefen und gegebenenfalls zu schaerfen.

