# Ergebnisklassen-Mapping der Lab-Traeger (Coverage-Design, v2 container-treu)

Stand: 2026-06-16 · Revision nach Pilot Stufe 2. Die erste Fassung (v1,
2026-06-15) wurde durch den Piloten widerlegt: das bare-container-Target
bildet nur **container-treue** Anforderungen faithful ab. Diese Fassung
verengt die Carrier entsprechend (vgl. `selection_log.json` →
`container_fidelity_rescope`; Pilot-Artefakte im Lab-Repo
[grundschutz-agent-lab](https://github.com/py-bay/grundschutz-agent-lab)).

## Container-Fidelitaet als harte Auswahlachse

Faithful im unprivilegierten ubuntu+sshd-Pod ist nur, was dort **beobachtbar**
ist: statische Konfig-Dateien, Paketstatus (`dpkg`), das real laufende sshd
(`sshd -T`), PAM-/login-/sudo-Konfiguration, Dateirechte, Trust-Store. Nicht
faithful (vom Piloten belegt): Host-/Kernel-Ebene (geteilter Node-Kernel,
welt-lesbar), Laufzeit-Dienste (kein Init/Daemon im Pod), Virtualisierung und
Docker-Host. Damit kollabieren die drei v1-Cluster faktisch auf **Linux-Server
und Linux-Client (Konfigauditing)**; der Virtualisierungs-Cluster entfaellt.

Pruefeinheit bleibt der **gewertete B-Satz** im Verbund mit einem
konstruierten Referenzzustand. Replikation 1/1/2/2/2 wie gehabt.

## Mapping (8 Items / 6 distinkte Anforderungen)

| Item | Ergebnisklasse | Soll-Urteil | Traeger | Gewerteter B-Satz | Container-treue Evidenz / Zielzustand |
|:----:|-------|-------------|---------|-------------------|----------------------------------------|
| 1 | 1 sauber konform | konform | SYS.2.1.A18 | A18.S02 | `sshd -T`: nur moderne Ciphers/MACs/KEX |
| 2 | 2 sauber nicht-konform | nicht konform | SYS.2.1.A18 | A18.S02 | `sshd -T`: schwache Verfahren (cbc/sha1/dh-group1) aktiv |
| 3 | 3 zu komplex | nicht konform | SYS.1.1.A2 | A2.S01 | Synthese PAM + login.defs + pwquality, eine subtile Schwaeche |
| 4 | 3 zu komplex | konform | SYS.1.1.A33 | A33.S02 | Trust-Store vs. dokumentierte Baseline, kein Rogue-CA |
| 5 | 4 fehlende Berechtigung | nicht verifizierbar | SYS.2.3.A1 | A1.S02 | sudo-Policy 0440 root-only (**pilot-validiert**) |
| 6 | 4 fehlende Berechtigung | nicht verifizierbar | SYS.1.1.A2 | A2.S01 | /etc/shadow 0640 root:shadow, Hash/Aging nicht lesbar |
| 7 | 5 nicht entscheidbar | nicht verifizierbar | SYS.1.1.A39 | A39.S01 | Einstellungen zentral verwaltet, Baseline off-host |
| 8 | 5 nicht entscheidbar | nicht verifizierbar | SYS.1.1.A19 | A19.S02 | Remote-Identitaet via zentralem Trust-Anker off-host |

SYS.1.1.A2 traegt zwei Items (3: lokale Auth-Policy-Synthese; 6:
Credential-Speicherung) in verschiedenen Ergebnisklassen mit verschiedener
Operationalisierung — analog zum A14-Muster der v1 (eine Anforderung, zwei
konstruierte Zustaende). SYS.1.1.A19: nur S02 (Remote-Identitaet) wird
gewertet, S01 (lokaler Paketfilter) ist nicht container-treu.

## Warum diese Zuordnung

- **Ergebnisklassen 1+2 (SYS.2.1.A18):** SSH-Krypto laeuft echt im Container und ist via
  `sshd -T` voll ablesbar; der A8-Durchstich beweist die Klasse. "Angemessen
  starke Algorithmen" ist eine echte B-Interpretation, der
  konform/nicht-konform-Kontrast am selben Traeger deckt einen konstant
  urteilenden Agenten auf (DZ4).
- **Ergebnisklasse 3 (A2, A33):** echte Mehrquellen-Synthese aus statischen,
  container-lesbaren Konfigdateien. Gegenlaeufige Soll-Urteile (nicht_konform
  via Auth-Policy, konform via Trust-Store) schliessen die
  Idiosynkrasie-Rivalenerklaerung aus.
- **Ergebnisklasse 4 (A1, A2/shadow):** Evidenz existiert real, ist aber per **echtem
  Default** root-only (sudoers 0440, shadow 0640 root:shadow) — keine
  konstruierte Sperre, kein Laufzeit-Widerspruch, kein welt-lesbarer Shortcut.
  A1 ist pilot-validiert.
- **Ergebnisklasse 5 (A39, A19):** maelgebliche Instanz liegt prinzipbedingt off-host
  (zentrales Management, zentraler Trust-Anker). On-host nur der Verweis →
  echte Nicht-Entscheidbarkeit, kein konstruiertes Loch.

## Verworfene v1-Traeger (Pilot-Befund)

- SYS.1.3.A17 (Kernel-Haertung), SYS.1.5.A22 (Host-Haertung): geteilter
  Host-Kernel, welt-lesbar → Agent urteilt korrekt nicht_konform.
- SYS.2.1.A45 (Logging), SYS.1.1.A6 (Dienste): Laufzeit-Dienste, im bare
  container nicht aktiv → beobachtbar nicht_konform.
- SYS.1.5.A2 (VM-Isolation), SYS.1.6.A5 (Container-Netz): Virtualisierung /
  Docker-Host, nicht container-treu.
- SYS.2.3.A14 (Geraete-/USB-Kontrolle): `lsmod` zeigt Host-Module, usbguard
  ist Daemon → ersetzt durch SYS.2.1.A18 fuer die Ergebnisklassen 1/2.

## Validitaetsimplikation

Der Lab-Perimeter ist enger als das A/B/C-Schema: bewertet wird der
**container-pruefbare Anteil der B-Klasse** (statische Konfig-, sshd-, PAM-,
sudo-, Trust-Store-Evidenz auf Linux-Servern/Clients). Host-/Kernel-Ebene,
Laufzeit-Dienste, Virtualisierung und Multi-Host liegen ausserhalb. Der
container-treue ∩ B ∩ SYS-Raum ist schmal — das Set stuetzt sich auf
wenige Anforderungen (v.a. SYS.1.1.A2). Beides ist im Methodikkapitel der
Arbeit als deklarierte Validitaetsgrenze ausgewiesen.

## Status nach dem Hauptlauf

- Die Items 1-4, 6 und 7 bildeten den gewerteten Hauptlauf der Arbeit:
  fuenf Operationalisierungen ueber vier distinkte Anforderungen, je ein
  adversariales Variantenpaar, also zehn Prueffaelle mit k = 4
  Wiederholungen. Konstruktion und Einzelfall-Validierung der
  Referenzzustaende sind im Lab-Repo dokumentiert.
- Die Items 5 (SYS.2.3.A1, pilot-validiert) und 8 (SYS.1.1.A19) liegen
  ausserhalb des gewerteten Hauptsatzes; sie dienen in der Diskussion der
  Arbeit als fehlerinduzierende Grenzfaelle.
- Die qualitative Zweitkodierung der Klassenzuordnungen und die externe
  Plausibilisierung der Kern-Items durch einen unabhaengigen Praktiker
  blieben offen und sind in der Arbeit als Limitation der
  Konstruktvaliditaet ausgewiesen.
