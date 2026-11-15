# Projekt-Abstrakt: Hisense VIDAA Clean Home

[English](PROJECT-ABSTRACT.md) · [Masterprompt](MASTERPROMPT.md) · [Kompatibilität](COMPATIBILITY.md)

**Stand: 15. November 2026.** Diese Übergabe bündelt die technischen Erkenntnisse,
Recherche, erfolgreichen Wege und Fehlschläge des Projekts. Persönliche Daten,
Zugangsdaten, private Geräteinhalte und der Wiedergabeverlauf sind ausgelassen.
Die technischen VIDAA-Schnittstellen und Modell-/Firmwareangaben bleiben als
übertragbares Wissen erhalten.

## Ziel und Ergebnis

Auf einem Referenzfernseher wurde die native VIDAA-Startseite zu einem
schwebenden, anpassbaren App-Dock umgebaut. Die physische Home-Taste führt über
die vorhandene Systemoberfläche direkt zurück. Der frühere Umweg über einen
neu geöffneten Browser entfällt.

Die vorhandenen Streaming-Apps, Anmeldung, Jugendschutz, DRM, Einstellungen und
Update-Konfiguration bleiben Teil des Systems. Es wurde kein anderes
Betriebssystem installiert. Das Projekt ist ein nativer Homescreen-Umbau mit
optionalen Zusatzfunktionen und separater DNS-Filterung.

Die bestätigte Referenz ist eine Einheit mit **MTK9602, VIDAA U9,
V0000.09.09F.P0930 und interner Modellfamilie 43A53FEVS_0004**. Die
Verkaufsbezeichnung wurde nicht abschließend verifiziert. Ein anderes Gerät mit
VIDAA oder demselben Chip ist dadurch noch nicht kompatibel.

## Der ehrliche Funktionsstand

| Funktion | Nachweis |
| --- | --- |
| Schwebendes Dock, App starten und Home-Rückkehr | Auf dem Referenzgerät bestätigt |
| Favoriten verschieben/ausblenden mit langem OK; App Store | Bestätigt |
| Eingänge als normal navigierbares Raster | Bestätigt |
| Animiertes Hintergrundvideo in Schleife | Bestätigt |
| Regenvideo als manuell gestarteter Bildschirmschoner; Zurück | Bestätigt |
| Jellyfin als App-Kachel mit lokalem Server | Bestätigt, separate Erweiterung |
| Netflix-Vorschau mit Titel, Bild und Aufruf | Bestätigt; genaue Folge und Restzeit offen |
| Prime-Vorschau mit Titel, Bild, Staffel/Folge und Aufruf | Bestätigt; Restzeit offen |
| Disney-Vorschau mit Bild, Staffel/Folge, Restzeit, Fortschritt und richtiger Folge | Vom Besitzer bestätigt; private Anbindung |
| YouTube „Zuletzt angesehen“ | Versuch nicht akzeptiert: Karte fehlte oder zeigte den falschen Inhalt |
| Persönliche Vorschau für ARD, ZDF, RTL+, MagentaTV, HBO Max | Nicht bestätigt |
| Gemeinsame Auswahl eigener Videos für Hintergrund und Schoner | Vorbereitet und offline getestet; Nutzung am Gerät nicht bestätigt |
| Automatischer Schoner nach zehn Minuten im Home | Reeller Zehn-Minuten-Test offen |
| Eigener Schoner bei pausiertem Netflix mit zuverlässiger Rückkehr | Nicht gelöst |
| Verallgemeinerte öffentliche Version | Offline getestet; nicht als neuer Build am TV abgenommen |
| Funktion auf allen VIDAA-Geräten | Nicht belegt |

Die privaten Anbieter-Anbindungen für „Weiterschauen“ sind **nicht im
öffentlichen nativen Build enthalten**. Diese Übergabe erklärt ihre Erkenntnisse
und den nächsten Implementierungsweg. Dokumentation ist keine bereits
ausgelieferte Funktion.

## 1. Der entscheidende Wechsel vom Browser zur nativen Oberfläche

Anfangs konnte eine gekoppelte Fernsteuerung Apps öffnen und eine Browserseite
starten. Ein Beobachter reagierte auf stock Home und öffnete diese Seite erneut.
Das führte zum sichtbaren Umweg über VIDAA und zu erneutem Laden. Ein kürzeres
Abfrageintervall hätte das Grundproblem nicht beseitigt. Auch der untersuchte
Debug-Aufruf zeigte auf dieser Firmware nicht den erwarteten Installer.

Der funktionierende Weg behielt die native Engine, das Hersteller-Bundle und
seine Modulregistrierung. Über einen Wrapper um `_V_M_.launcher` wurde die
Vue-Komponente `/Launcher` ausgetauscht; die vorhandene `_V_SDK_`-Umgebung blieb
erhalten. Die Home-Taste landete damit direkt in der angepassten nativen Ansicht.
Der Schoner wurde unabhängig davon über sein eigenes Modul eingebunden.

Der Browser war beim Aufbau des Wartungszugangs beteiligt. Das bedeutet nicht,
dass der fertige Homescreen im Browser läuft.

## 2. Wartungszugang, Backups und Wiederherstellung

Eine vorhandene Datei-/Dienstschnittstelle diente zur Untersuchung. Ein lokales
Diagnosepaket lieferte anschließend einen unabhängig zurückgelesenen Nachweis,
dass sein Installationsskript mit UID 0 lief. Die äußere Paketmeldung allein war
kein zuverlässiger Nachweis: Ein Fehler konnte erscheinen, obwohl ein Teil bereits
ausgeführt worden war. Deshalb keine blinden Installationswiederholungen.

Danach wurde ein zeitlich begrenzter, schlüsselbasierter Wartungszugang verwendet,
auf den Wartungsrechner eingeschränkt und ohne dauerhaften Autostart. Vor dem
Home-Umbau wurden Originale, Prüfsummen, Dateirechte und die tatsächliche
Start-/Cache-Struktur gesichert.

**Der Intel-Mac war der Arbeits- und Serverrechner. Er war nicht die Ursache,
warum der Zugriff auf dieser Firmware gelang.** Ausschlaggebend waren die
Schnittstellen und Berechtigungen des Fernsehers. Auch ein anderer geeigneter
Rechner kann bauen, Dateien bereitstellen und einen freigegebenen Zugang bedienen.

Backups sind notwendig, garantieren aber allein keine Wiederherstellung: Der
Rückweg muss auch funktionieren, wenn Home kaputt ist. Kandidaten neben dem Ziel
vorbereiten, mit korrekten Rechten atomar umbenennen und nur die tatsächlich
identifizierte Engine neu laden. Ein GUI-Neustart kann einen Film unterbrechen.

Alte komplette Cache-Sicherungen dürfen keinen neueren Schoner zurücksetzen.
Caches müssen zu den aktuell vorhandenen Modulen passen. Ein angekündigter
Rollback ist noch kein nachträglich verifizierter Rückbau. Ein geschlossener
Wartungsport beweist ebenfalls nicht, dass jedes Diagnosepaket entfernt wurde.

## 3. Erkenntnisse vom anderen Fernseher

Für einen 50E6NT wurde `V0002.09.60A.Q0707`, intern `50A60LEVS_0002`, mit
MTK9603 gemeldet. Die dokumentierte Entwicklung ging von Informationsabfragen
über funktionierende Dateilesungen und verifizierten Quelltexttransfer zu zwei
Schreib-/Rücklese-/Aufräumtests mit harmlosen Markern. Später wurde ein einmaliger
UID-0-Nachweis aus einem Diagnosepaket berichtet.

Dabei wurden mehrere falsche Sackgassen korrigiert:

- Eine fehlende WebSDK-Funktion bedeutete nicht, dass vowOS/HiUtils ebenfalls
  unbrauchbar war.
- Das Wort `permission` innerhalb erfolgreich gelesenen Quelltexts wurde
  fälschlich als Zugriffsverweigerung erkannt. Entscheidend ist die strukturierte
  Antwort mit ihrem echten Ergebnis.
- `ENOENT` bedeutet, dass der konkrete Pfad fehlt. Daraus folgt nicht, dass alle
  Dateien oder alle App-Registrierungen unerreichbar sind.
- Abfotografierter und abgetippter Quelltext war nicht bytegleich. Direkter
  privater Transfer mit gleichen Zeichen-/Bytezählungen und Prüfsummen beseitigte
  diese Unklarheit. Für Originale und Builds SHA-256 verwenden.
- Erst der vollständige Dispatcher klärte die Argumentform. Ein isoliertes
  Funktionsfragment reichte nicht für den gesamten Aufrufvertrag.
- Quellen und Tests zeigten für diesen Dienst eine einmalige Registrierung ohne
  zusätzlichen Start. Das ist keine Aussage über jeden VIDAA-Dienst.
- HTTP 501 beim Hochladen lag am lokalen Empfänger, der POST nicht unterstützte.
  Das war kein Rechtefehler des TVs.
- Asynchrones Aufräumen musste durch erneutes Lesen und bestätigtes Fehlen
  geprüft werden. Ein Rückgabewert allein war kein Löschbeweis.
- Doppelte Anfragen und erneutes Ablegen nach Seiten-Reload blieben ungeklärt.
  Diagnose-Seiten dürfen beim Laden keine Änderungen ausführen; Aktionen brauchen
  eindeutige Zuordnung und Schutz vor Wiederholung.
- Nach einem belegten Root-Test folgt die Klärung von Zugang, Aufräumen,
  Sicherungen, Wiederherstellung und nativer Portierung. Weitere Root-Beweise
  verschwenden Zeit und erhöhen unnötig die Zahl der Eingriffe.

Das sind **Besitzerberichte**, hier nicht unabhängig reproduziert. Das spätere
Aufräumen des Diagnosepakets wurde vorbereitet, aber nicht als abgeschlossen
gemeldet. Ein nativer Home-Umbau auf diesem Gerät ist damit noch nicht bestätigt.

### Weitere Erfolgsmeldung: 55U7Q

Der Besitzer des 55U7Q mit `V0000.09.60A.Q0602` und erweiterter Version
`X0003.W01.Y01.J01` meldet inzwischen eine erfolgreiche Einrichtung und hat ein
Foto mit sichtbarem Dock geschickt. Damit ist der frühere Stand „nur
Identitätsangaben“ überholt. Die positive Rückmeldung wird als Community-Ergebnis
mit sichtbarer Oberfläche festgehalten.

Projekt-Revision, interne Modellkennung, Chip, Original-Hashes und Zugangsweg
wurden nicht mitgeteilt. Native Home-Rückkehr, Neustart-/Standby-Verhalten,
Wiederherstellung und Zusatzfunktionen sind nicht einzeln bestätigt. Ein neues
Referenzprofil oder allgemeine Kompatibilität ergibt sich daraus nicht.
Die [55U7Q-Nachweise](COMPATIBILITY.md#community-case-55u7q) trennen diese Punkte.
Die private Nachricht, das Foto und der Accountname werden nicht veröffentlicht.

Auf dem bereits funktionierenden Gerät bleiben Einrichtung und private Nachweise
erhalten; nur fehlende Funktionsbestätigungen werden ergänzt. Kein erneuter
Root-Test oder Neuaufbau allein für die Dokumentation. Auf einem anderen Gerät
dient die Meldung als gezielter Recherchehinweis, dessen eigene Schnittstellen
weiter zu prüfen sind. Die Anfrage zum 32-Zoll-E5ST bleibt ohne Erfolgsmeldung.
Ähnliche Versionsnummern beweisen keine gleichen Berechtigungen.

## 4. Gestaltung und Bedienung des Docks

Das Zielbild ist eine einzige frei schwebende horizontale App-Reihe ohne
umgebenden Dock-Rahmen. Seitlich werden Kacheln weich ausgeblendet. Die ausgewählte
App ist etwas größer und erhält als einzige den bewegten Metallrand.

Oben bewegt sich ein gemeinsamer Rahmen zwischen Apps, Eingänge und Fernseher.
Die Tastatur-/Fernbedienungsfokussierung muss sich sichtbar von einer bloß
ausgewählten Rubrik unterscheiden. Langes OK öffnet Verschieben/Ausblenden und
darf anschließend nicht noch einen normalen App-Start auslösen.

Die tatsächliche App-Liste des Geräts ist maßgeblich. Eine feste Beispiel-Liste
hatte unerwünschte Apps erzeugt. Store-Eintrag und App-IDs werden aus dem Gerät
bestätigt; Entfernen aus Favoriten deinstalliert keine System-App.
Bildobjekte werden über Rubrikwechsel behalten. Im Eingänge-Raster bewegen
Auf/Ab den Fokus spaltenweise, auch bei einer unvollständigen letzten Reihe.

Schrift wird nativ und getrennt vom Video gerendert. Ein niedrig aufgelöstes
Canvas großzuziehen war kein Weg zu scharfer Schrift. Die beobachtete native
Oberfläche hatte 1920×1080 logische Pixel; daraus folgt keine native 4K-Ausgabe.

Die Optik orientiert sich an [Libraries.dev](https://libraries.dev/) und Liquid
Metal. Für den TV wurden kleine vorberechnete Effektbilder verwendet. Ein
React-/WebGL-Effekt lässt sich nicht unverändert in die native Engine einsetzen.
Große Atlanten und Überblendungen führten zu Blinken oder Ruckeln. Die akzeptierte
Referenz verwendete 24 Bilder, 200 ms pro Bild vor/zurück und einen separaten
220-ms-Fokuswechsel. Das ist ein ressourcensparender Kompromiss.

## 5. Warum das Hintergrundvideo schließlich lief

Die entscheidende Erkenntnis war die Kombination aus richtig zugeordneter
nativer Wiedergabesitzung und einer transparenten Kette von Home-Elternelementen.
Ein laufender Player konnte hinter einer undurchsichtigen Oberfläche unsichtbar
bleiben. PLAYING und fortschreitende Zeit waren deshalb noch kein Sichtnachweis.

Der native Ablauf wurde aus der tatsächlichen Firmware-Implementierung
hergeleitet: eigene DMP-Sitzung, bestätigter Quellenwechsel, lokale Datei mit
`?video-play-mode=1`, passende PREPARED-/PLAY-Ereignisse und Aufräumen nur des
eigenen Players. Hersteller-Bundles oder Werbedienst-Code werden nicht verteilt.

Das Video wird einmal auf dem Rechner als stummes H.264-MP4 vorbereitet,
auf der Referenz 1080p24. Leichte Verlangsamung und eine kurze Überblendung zwischen
Ende und Anfang werden in die Datei eingerechnet. Bekannte Schleifenlänge und
wiederholte Fortsetzung erlauben den Sprung vor dem Dateiende.
GIF, 4K-Canvas-Dekodierung und geratene Schleifenzeiten sind keine Abkürzung.

Die dunkleren Schwarztöne wurden durch eine lokale Schattenkorrektur im Video
erreicht, nicht durch einen schwarzen Layer über der ganzen Oberfläche.
Diese spezielle Farbkorrektur gehört bislang nicht zum öffentlichen Exporter.

## 6. Bildschirmschoner und eigene Medien

Der manuelle Einstieg musste das tatsächliche Schoner-Modul öffnen:
`sdk.me.req('screen-saver').open('screenMode', {from:'launcher'})`.
Ein ähnlich aussehender Router-Pfad innerhalb des Launchers öffnete das falsche
Modul. Der Schoner braucht seinen eigenen Videohelfer und muss unabhängig von
der vorherigen Home-Ladereihenfolge funktionieren.

Das Regenvideo und die Rückkehr mit Zurück wurden bestätigt.
Der automatische Start nach zehn Minuten Home-Leerlauf wurde nicht abschließend
geprüft. Ein pausierter Netflix-Film ist ein anderer Fall: Ein nativer
Quellenwechsel kann dessen DRM-/Wiedergabesitzung stören. Ein einfacher Timer
ohne Tastendruck erkennt keine zuverlässige Filmpause.

Die gemeinsame Medienauswahl ist vorbereitet: Ein Clip kann für Home und Schoner
verwendet werden, mit unabhängiger Auswahl und nur einer gespeicherten Kopie.
Vor dem tatsächlichen Einsatz sind freier Speicher und Gerätetest erforderlich.
Originalvideos und kostenpflichtige Icon-Pakete werden nicht mitgeliefert;
Quellseiten und die Anleitung für eigene Medien stehen im Repo.

## 7. Jellyfin

Jellyfin wurde als App-Eintrag mit Web-Client und lokalem Server eingebunden.
Das ist keine Android-App-Datei. App-Registrierung, Favoriten, Icon-Cache und
tatsächlicher Start mussten separat geprüft werden.

Ein Link konnte Jellyfin öffnen, obwohl die erste Installationsseite die normale
Installationsfunktion nicht fand. Eine erfolgreiche Browseröffnung war deshalb
kein Beweis für die fertige Home-Kachel. Eine leere Bibliothek wiederum war kein
Netzwerkfehler. Die spätere Kachel, Anmeldung und Nutzung wurden bestätigt.

Die vorhandene Home-Konfiguration wurde für diese einzelne Ergänzung beibehalten.
Die [Jellyfin-VIDAA-Anleitung](https://github.com/theDavidCoen/jellyfin-vidaa-install)
dient als Recherchequelle; ihre DNS-Umleitung muss nicht auf ein bereits
funktionierendes natives Setup übertragen werden. Serveradressen, Konten und
Quick-Connect-Zustand bleiben privat. Medien-/Codec-Wiedergabe wird separat geprüft.

## 8. „Weiterschauen“ und Anbieter-Recherche

Die akzeptierte kleine Karte misst 720×190 logische Pixel, mit einem vollständig
eingepassten Bild von 288×162 und Innenabstand. Titel, Staffel/Folge, Restzeit und
Fortschritt sollen in derselben Größe Platz finden. Die transparente Glasoptik
braucht eine einfache Alternative, wenn Blur nicht unterstützt wird.
Ein CSS-Hintergrund funktionierte auf der nativen Engine, während ein Bild-Element
zunächst leer blieb.

Jeder Anbieter benötigt einen eigenen Datenadapter. Gemeinsam normalisiert
werden App-/Inhaltszuordnung, Titel, Bild, tatsächliche Episode, Zeitdaten,
Gültigkeit und nativer Aufruf. Ein verspätetes Ergebnis darf nach Fokuswechsel
nicht unter der falschen App erscheinen. Konto-/Profilwechsel müssen alte
Daten verwerfen. Wartungsfrist und Inhaltsgültigkeit sind getrennte Größen.

Netflix liefert bestätigte persönliche Vorschauen mit Bild und Aufruf. Die
native Partner-/DET-Anmeldung ist nicht mit Website-Cookies austauschbar.
Katalogzahlen für Staffeln/Folgen und ein Balken im Vorschaubild beweisen keinen
konkreten Wiedergabezeitpunkt. Home-Neustarts können neue Anbieterabfragen
auslösen und damit die nächste erlaubte Aktualisierung verschieben.
Weitere Restzeit-/Folgenfelder sind nicht zuverlässig nachgewiesen.

Prime lieferte nach Zuordnung zur exakten nativen Inhaltsaktion Staffel/Folge
aus Katalog-Dekorationen. Restzeit bleibt offen. Ein TV-Token funktionierte nicht
an einer anderen mobilen API; Kodi-Wiedergabedaten wären ebenfalls nicht der
Verlauf der TV-App.

Disney wurde mit Bild, Staffel/Folge, Restminuten, Fortschritt und richtiger
Folge plus Home-Rückkehr bestätigt. Diese funktionierende private Anbindung
bleibt die Referenz; sie ist keine frei verfügbare universelle Disney-API.

Jellyfin besitzt eine eigene Resume-API. Ohne Inhalte in der Bibliothek gab es
hier noch keinen echten fortsetzbaren Titel für die Vorschau-Abnahme.

Bei YouTube wurden eine persönliche Verlaufsantwort, Bildabruf und
Token-Erneuerung technisch erreicht. Die Karte war für den Nutzer jedoch fehlend
oder falsch und damit nicht akzeptiert. Aktives TV-Profil, sichtbarer Treffer und
direkter Videoaufruf bleiben offen. Die offizielle Data API stellt den
Wiedergabeverlauf nicht bereit; die untersuchte TV-History ist ein separater Weg.

Für ARD, ZDF, RTL+, MagentaTV und HBO Max ist keine persönliche Vorschau bestätigt.
Eine installierte App oder eine Empfehlungsreihe ersetzt diesen Nachweis nicht.

Alle Quellen, Datenverträge und Prüfschritte stehen in
[CONTINUE-WATCHING.md](CONTINUE-WATCHING.md). Private Titel, Verlauf, Anmeldedaten
und signierte Links sind nicht enthalten.

## 9. Anleitung und Arbeitsweise des Coding Agents

Der Agent soll zielstrebig ausführen, vorhandene Erfolge nutzen und nach einem
klar eingegrenzten Fehlschlag die nächste begründete Möglichkeit untersuchen.
Ein fehlender Modell-Eintrag beendet nicht die Recherche. Gleichzeitig werden
keine Simulationen als Geräteerfolg ausgegeben und keine fremden Firmwarewerte
hineinkopiert, um eine Prüfung künstlich zu bestehen.

1. Repo und Masterprompt lesen. Bei bestehenden Arbeiten zuerst die private
   Übergabe, gültige Prüfergebnisse, Zugangsfrist und Aufräumstatus lesen.
2. Skripte prüfen und bei einer neuen Installationsanfrage
   `python3 agent.py start --json` ausführen. Bei reiner Repo-/Simulationsarbeit
   keine Verbindung zum Fernseher aufbauen.
3. Vorhandene Gerätedaten und Freigaben wiederverwenden. Nur tatsächlich fehlende
   Informationen ermitteln. Hypothese, Beleg, Ergebnis und nächste Aktion notieren.
4. Transport, Argumentform, Leserecht, Schreibrecht, Dienstlebenszyklus,
   Paketausführung, Root, Wiederherstellung und Home-Portierung separat bewerten.
5. Funktionierende Leseschnittstellen bevorzugen. Quellen vollständig und
   verifiziert übertragen; unabhängige Lesungen bündeln.
6. Neue Eingriffe konkret vorbereiten. Schreibaktionen nacheinander ausführen,
   unklare Ergebnisse vor Wiederholung abgleichen und Aufräumen nachprüfen.
7. Nach Root-Nachweis zu Sicherungen, unabhängigem Rückweg und geräteeigenem
   nativen Kandidaten übergehen. Keine endlosen erneuten Root-Tests.
8. Zuerst statisches Home, dann Video und optionale Anbieterfunktionen prüfen.
   Bereits akzeptierte Funktionen dabei bewahren.
9. Sichtbares Ergebnis, richtige Inhalte/Aktionen und App → Home testen.
   Test-Rollback ausdrücklich annehmen/auflösen, bevor normales Fernsehen beginnt.
10. Nur bereinigte Dokumentation und generischen Code veröffentlichen.
    Konkrete offene Abhängigkeiten und den nächsten vorbereiteten Schritt nennen.

Die Offline-Prüfungen sind `node check.mjs`, `python3 check.py`,
`python3 privacy-check.py` und `python3 agent.py simulate --json`.
Simulationsergebnisse werden behalten und bei gleichen Bedingungen wiederverwendet.
Sie beweisen keine echte Firmware-Berechtigung, Wiederherstellung oder
DRM-/Decoder-Kompatibilität.

## 10. Datenschutz, Lizenz und Grenzen

Keine Passwörter, Schlüssel, Tokens, Seriennummern, Geräte-IDs, IP-/MAC-Adressen,
privaten Rechnerpfade, Konten, Wiedergabeverläufe, Chatbilder oder Geräte-Dumps
veröffentlichen. Auch eine Herstellerdatei kann private Kontoinformationen
enthalten. Technische VIDAA-Erkenntnisse werden zusammengefasst; Rohdaten bleiben
privat. Die ausdrücklich freigegebene Repo-Vorschau ist ein separater Fall.

Neue eigene Beiträge stehen im bestehenden Umfang unter PolyForm Noncommercial.
Frühere MIT-Rechte und fremde Lizenzhinweise bleiben erhalten. Das macht private
Videos oder gekaufte Icons nicht automatisch weiterverteilbar.

Der saubere Homescreen entfernt die Werbung aus dieser Ansicht. Zusätzliche
DNS-Filter können bekannte Domains gezielt für den TV blockieren. Daraus folgt
keine Garantie gegen sämtliches Tracking, Datenverkauf oder Werbung innerhalb
von Streaminginhalten. ACR-/Mikrofoneinstellungen sind getrennte Themen.
Wenn nur ein Anbieter nicht funktioniert, wird dieser gezielt untersucht.

## Quellen und vollständige Detailanleitungen

- [MASTERPROMPT.md](MASTERPROMPT.md): operative Agent-Anweisung.
- [WORKED-EXAMPLE.md](WORKED-EXAMPLE.md): ursprünglicher Erfolg, native Verträge und Fehler.
- [ACCESS-RESEARCH.md](ACCESS-RESEARCH.md): alternative Schnittstellen und Community-Belege.
- [PORTING.md](PORTING.md), [RECOVERY.md](RECOVERY.md): anderer Build und Rückweg.
- [CONTINUE-WATCHING.md](CONTINUE-WATCHING.md): Anbieter-Recherche mit primären Quellverweisen.
- [ANIMATED-WALLPAPERS.md](ANIMATED-WALLPAPERS.md): eigene Videos vorbereiten.
- [VIDAA-MODELS.md](VIDAA-MODELS.md): Herstellerquellen, keine pauschale Kompatibilitätsliste.
- [LAB.md](LAB.md), [SIMULATION.md](SIMULATION.md): gespeicherte modellierte Ergebnisse.
- [PRIVACY.md](PRIVACY.md), [CREDITS.md](CREDITS.md): Veröffentlichungsgrenzen, Libraries.dev,
  alvidaa, Free My TV, Quellen und Lizenzen.

Der übertragbare Erfolg ist ein belegbarer Arbeitsweg mit konkreten Schnittstellen
und Fehlerkorrekturen. Ob ein weiterer Fernseher denselben Weg erlaubt, muss
an seinem tatsächlichen Build festgestellt werden.
