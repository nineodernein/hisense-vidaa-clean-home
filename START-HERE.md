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

Den entpackten Ordner in **Codex** oder **Claude Code** öffnen. Der Computer muss
den Fernseher im eigenen Netzwerk erreichen können. Ein reiner Web-Chat hat
diesen Zugriff normalerweise nicht. Danach diesen Auftrag einfügen:

> Lies MASTERPROMPT.md und AGENTS.md. Prüfe meinen eigenen Hisense VIDAA und
> richte den nativen App-Dock-Homescreen ein, wenn die Kompatibilität nachgewiesen
> ist. Sichere die Originale privat. Zeige mir vor Systemänderungen den konkreten
> Plan und den Rückweg. Andere Geräte und Routereinstellungen bleiben unverändert.

## 3. Die notwendigen Angaben

Der Agent braucht Modell und vollständige Firmwareversion, die IP des TV und
einen bereits erlaubten Wartungszugang oder einen nachvollziehbaren Weg dafür.
Seriennummer, Netflix-Passwort, Router-Passwort und private Kontodaten gehören
nicht in ein öffentliches Issue. Gib Passwörter nicht als Teil des Masterprompts
an; lokale Schlüssel und Konfiguration bleiben privat.

Der aktuelle Build unterstützt nur die Originaldateien aus compatibility.json.
„Hisense“ oder „VIDAA“ allein reicht nicht. Bei einer Abweichung bricht der Build ab.

## 4. Erst offline prüfen und bauen

Python 3.10+ und Node 18+ müssen auf dem Computer vorhanden sein.
Der Agent darf fehlende Programme nicht heimlich installieren.

```sh
node check.mjs
python3 check.py
python3 privacy-check.py
mkdir -m 700 .private
cp config.example.json .private/ui.json
```

Der Agent sichert Home/Saver vom eigenen TV nach .private/stock und prüft die
Hashes. Mit passenden Originalen:

```sh
node build.mjs --config .private/ui.json --out .private/build-first
```

Das erzeugt ein **privates** TV-Bundle; noch keine Installation.
Diese Dateien enthalten Hersteller-Code und bleiben bei dir.

## 5. Auf dem TV aktivieren

Das ist der geräteabhängige Schritt. Der Agent folgt NATIVE-ACCESS.md und
RECOVERY.md, prüft Root-Zugang/Dateipfade, legt den Rückweg an und überträgt nur
die freigegebenen Module und Assets. Er startet die native Oberfläche kontrolliert
neu. Dieser Vorgang kann eine laufende App unterbrechen.

Es gibt absichtlich keinen universellen Download-Knopf „alle Hisense entsperren“.
Ein passender, begrenzter Wartungszugang ist Voraussetzung. Wenn der fehlt,
kannst du unabhängig davon den DNS-Weg aus DNS.md verwenden.

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
