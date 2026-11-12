# Herunterladen, vorbereiten und aktivieren

## 1. Das Repository herunterladen

Auf der GitHub-Startseite oben **Code** anklicken, danach **Download ZIP**.
Die ZIP-Datei auf deinem Mac, Linux-PC oder Windows-PC entpacken.
Alternativ mit installiertem Git:

```sh
git clone https://github.com/nineodernein/hisense-vidaa-clean-home.git
cd hisense-vidaa-clean-home
```

Es wird dadurch noch nichts am Fernseher installiert. Eine ZIP lässt sich nicht
einfach als TV-Firmware einspielen. Keine .bin/.pkg-Datei auf Verdacht flashen.

## 2. Dem Coding Agent Zugriff auf den Projektordner geben

Du kannst dem Agent auch direkt den Repo-Link mit dem Auftrag zum Einrichten
geben. [AGENT-START.md](AGENT-START.md) erklärt ihm den automatischen lokalen
Einstieg; Herunterladen und Befehle ausführen übernimmt er mit seinen Werkzeugen.

Den entpackten Ordner in **Codex** oder **Claude Code** öffnen. Der Computer muss
den Fernseher im eigenen Netzwerk erreichen können. Ein reiner Web-Chat hat
diesen Zugriff normalerweise nicht. Danach diesen Auftrag einfügen:

> Lies AGENT-START.md, MASTERPROMPT.md und AGENTS.md. Starte selbst die Offline-Prüfung. Untersuche meinen eigenen Hisense VIDAA nach ACCESS-RESEARCH.md: nutze bekannte Angaben weiter, prüfe konkrete Schnittstellen und verfolge nach einem Fehlversuch den nächsten belegten Ansatz. Richte den nativen Dock ein, sobald Zugang, Kompatibilität und Rückweg geprüft sind. Sichere Originale privat und zeige mir vor Systemänderungen den konkreten Plan. Andere Geräte und Routereinstellungen bleiben unverändert.

## 3. Die notwendigen Angaben

Der Agent beginnt mit Modell und vollständiger Firmwareversion. Für erlaubte
Geräteabfragen braucht er die bekannte TV-Adresse. Ein vorhandener
Wartungszugang hilft; fehlt er, untersucht der Agent die Wege aus
ACCESS-RESEARCH.md. Bereits bekannte Angaben müssen nicht erneut eingegeben werden.
Seriennummer, Netflix-Passwort, Router-Passwort und private Kontodaten gehören
nicht in ein öffentliches Issue. Gib Passwörter nicht als Teil des Masterprompts
an; lokale Schlüssel und Konfiguration bleiben privat.

Der feste Referenz-Build akzeptiert nur die Originaldateien aus compatibility.json.
Bei einer Abweichung endet dieser Build-Pfad. Der Agent forscht weiter und
verwendet PORTING.md für eine getrennte Anpassung mit den eigenen Originaldateien.
„Hisense“ oder „VIDAA“ allein ist keine Installationsfreigabe.

## 4. Erst offline prüfen und bauen

Python 3.10+ und Node 18+ müssen auf dem Computer vorhanden sein.
Der Agent darf fehlende Programme nicht heimlich installieren.

```sh
python3 agent.py start --json
```

Ohne TV-Kontakt läuft nur die Prüfung und Simulation; anschließend werden leere
Vorlagen unter .private/ angelegt. Fehlende Programme werden gemeldet, nicht
automatisch installiert. Für eine reine Simulation ohne Vorlagen:

```sh
python3 agent.py simulate --json
```

Mit erlaubtem Lesezugriff sichert der Agent Home/Saver nach .private/stock und
füllt .private/device.json aus echten Beobachtungen. Die Originaldateien,
Firmware, Dateirechte, freier Speicher, App Store und der Rückweg werden geprüft.
Danach:

```sh
python3 agent.py prepare --json
```

Das erstellt zusätzliche Sicherungskopien, ein **privates** TV-Bundle und einen
Prüfplan; noch keine Installation. Diese Dateien enthalten Hersteller-Code und
bleiben bei dir. Der gemeldete Plan lässt sich vor einer Übertragung erneut prüfen:

```sh
python3 agent.py verify-plan --plan .private/plans/<id>.json
```

`<id>` durch den tatsächlich ausgegebenen Namen ersetzen. Der Check bestätigt nur
die lokalen Dateien; der aktuelle TV-Zustand muss separat geprüft werden.

## 5. Auf dem TV aktivieren

Das ist der geräteabhängige Schritt. Der Agent folgt NATIVE-ACCESS.md und
RECOVERY.md, prüft Root-Zugang/Dateipfade, legt den Rückweg an und überträgt nur
die freigegebenen Module und Assets. Er startet die native Oberfläche kontrolliert
neu. Dieser Vorgang kann eine laufende App unterbrechen.

Es gibt absichtlich keinen universellen Download-Knopf „alle Hisense entsperren“.
Ein passender, begrenzter Wartungszugang ist Voraussetzung. Wenn der fehlt,
folgt der Agent zunächst ACCESS-RESEARCH.md. Den unabhängigen DNS-Weg aus DNS.md
kannst du zusätzlich oder als bewusst gewählte Alternative verwenden.

## 6. Den Dock bedienen

- Links/rechts: Apps auswählen.
- OK kurz: App öffnen.
- OK länger halten: Verschieben oder vom Startbildschirm entfernen.
- Beim Verschieben links/rechts, OK bestätigt, Zurück verwirft.
- Hoch: Tabs; Runter: wieder in die App-Reihe.
- App Store steht rechts, wenn auf deinem Modell vorhanden.
- Apps bleiben installiert, wenn du nur ihren Favoriten entfernst.

Vor dem Übernehmen Home, App-Start, Eingänge und Zurück prüfen.
Den befristeten Testwächter ausdrücklich beenden/akzeptieren, bevor du wieder
einen Film schaust. Sonst kann seine automatische Rücknahme den Film unterbrechen.

## 7. Eigene animierte Bilder

Eigene Videodatei bereitstellen und ANIMATED-WALLPAPERS.md folgen. Die privaten
Beispielvideos und Icon-Pakete aus dem Screenshot werden nicht heruntergeladen.

## 8. Wieder entfernen

RECOVERY.md beschreibt das Zurücksetzen auf deine gesicherten Originalmodule.
DNS-Regeln separat entfernen beziehungsweise die zuvor notierte TV-DNS-Einstellung
wiederherstellen. Ein Factory Reset ist nicht der normale Rückweg.
