# Hisense VIDAA: eigener Homescreen statt Werbung

[English](README.md) · [Agent-Einstieg](AGENT-START.md) · [Masterprompt](MASTERPROMPT.md) · [Einfache Anleitung](START-HERE.md) · [Simulation](SIMULATION.md)

Dieses Projekt erklärt Coding Agents, wie sie auf einem **kompatiblen Hisense
VIDAA-Fernseher** eine eigene native Startseite mit einem App-Dock einrichten.
Dazu gehören langes OK zum Verschieben/Ausblenden, Eingänge, TV-Einstellungen,
App Store und eigene animierte Hintergründe.

![Eigener Hisense-VIDAA-Homescreen mit schwebendem App-Dock und animiertem Hintergrund](preview.jpg)

Die Vorschau zeigt das Referenzdesign. Die abgebildeten privaten Icons und das
Hintergrundvideo werden nicht als Dateien mitgeliefert. Standardmäßig werden
lokale TV-App-Icons oder Textkacheln genutzt.

## Einfach dem Coding Agent geben

```text
Use this: https://github.com/nineodernein/hisense-vidaa-clean-home
```

Der Einstieg enthält ein konkretes Ziel und einen ausführbaren Ablauf.
[Unsere funktionierenden Wege und die damaligen Fehler](WORKED-EXAMPLE.md)
sind dokumentiert. Bei anderen Geräten folgt der Agent dem
[Portierungsablauf](PORTING.md): eigene Originaldateien, passende SDK-Schnittstelle,
private Sicherung und separater Test. Ein anderes Modell beendet nicht einfach
die Recherche. Eine universelle Freigabe für jede Firmware ist das weiterhin nicht.
Die [gezielte Zugangsuntersuchung](ACCESS-RESEARCH.md) ergänzt konkrete
Leseaufrufe, getrennte HiUtils-/Fetcher-Wege und dokumentierte Fehldiagnosen.
Der Agent hält Ergebnisse fest und verfolgt bei einer gesperrten Schnittstelle
den nächsten durch Quellen begründeten Ansatz. Community-Meldungen werden
getrennt von bestätigten Installationen geführt.

Gib Claude Code oder Codex den Repo-Link mit dem Auftrag, es auf deinem eigenen
TV einzurichten. Der Agent soll zuerst selbst die lokalen Prüfungen starten.
Falls er den Link nur zusammenfasst, kopiere diesen kurzen Auftrag:

> Richte https://github.com/nineodernein/hisense-vidaa-clean-home für meinen eigenen TV ein. Folge AGENT-START.md und MASTERPROMPT.md und starte jetzt die Offline-Prüfungen. Untersuche fehlende Zugänge nach ACCESS-RESEARCH.md und verfolge nach einem fehlgeschlagenen Weg die nächsten durch Quellen begründeten Ansätze. Nutze vorhandene Angaben und Freigaben weiter. Sichere Originale privat und prüfe den Rückweg vor nativen Änderungen. Ändere keine anderen Geräte.

Der Agent bekommt Quellcode und konkrete Prüfschritte. Er muss nicht noch einmal
das ganze Projekt erfinden. Ein normaler Chat ohne Zugriff auf deinen Computer
und dein Netzwerk kann den Fernseher trotzdem nicht selbst ändern.

Der ausführbare Start mit vorhandenem Python 3.10+ und Node 18+ lautet:

```sh
python3 agent.py start --json
```

Er testet die Quellen und erstellt private, leere Vorlagen. `prepare` prüft später
die tatsächlichen Geräteangaben und Originaldateien, sichert sie erneut und baut
ein privates Paket. Diese Befehle nehmen keinen Kontakt zum TV auf. Die passende
Wartungsverbindung und eine geprüfte Installation bleiben geräteabhängig.
Eine bestandene Simulation ersetzt keinen Hardwaretest.

## Was funktioniert?

Am Referenzgerät wurden native Home-Rückkehr, App-Start, App-Favoriten bearbeiten,
Eingänge sowie ein lokales Video in Schleife und der manuelle Video-Bildschirmschoner
bestätigt. Das ist ein **nativer Umbau**, keine Browser-Umleitung.

Der veröffentlichte, verallgemeinerte Build ist offline geprüft, aber nicht als
neue Version auf dem Referenz-TV installiert. Die gemeinsame Medienauswahl ist
vorbereitet und offline getestet. Ein automatischer Regenvideo-Bildschirmschoner
bei pausiertem Netflix ist **nicht fertig**. Der reale Zehn-Minuten-Test auf Home
steht ebenfalls aus.

## Kann ich animierte Hintergrundbilder hinzufügen?

Ja. Eigene Videos werden lokal zu stummen H.264-MP4-Dateien mit 1080p/24 fps
aufbereitet. Ein JPG dient als Lade-/Fehlerfallback. Überblendung und eine kurze
zyklische Fortsetzung verringern sichtbare Sprünge beim Wiederholen.
Anleitung: [Animierte Hintergründe und Bildschirmschoner](ANIMATED-WALLPAPERS.md).

## Kann ich VIDAA-Werbung entfernen?

Für Home-Banner und bestimmte Empfehlungskacheln gibt es einen separaten
[DNS-Weg](DNS.md), auch ohne Root. Er wirkt nur auf den konfigurierten Fernseher.
Das ist keine Garantie gegen jede Werbung oder jede Datenübertragung.
Werbung innerhalb von Streamingvideos wird dadurch nicht zuverlässig entfernt.

## Passt das auf jeden Hisense?

Nein. Hisense verkauft unterschiedliche Betriebssysteme und Firmwarefamilien.
Getestet wurde eine interne Modellkennung 43A53FEVS_0004 mit MTK9602,
VIDAA U9 und P0930. Die Verkaufsbezeichnung allein reicht nicht.
[Kompatibilität prüfen](COMPATIBILITY.md).

VIDAA wird auch bei ausgewählten Fernsehern von Toshiba, Loewe/We. by Loewe,
MEDION und weiteren Marken verwendet. Das bestätigt nur das Betriebssystem,
nicht unseren nativen Umbau. Die [Modell- und Markenübersicht mit Herstellerquellen](VIDAA-MODELS.md)
trennt diese Geräte von der tatsächlich getesteten Referenz. Für andere Modelle
ist die Funktion dieses Docks bislang nicht bestätigt.

## Herunterladen und aktivieren

1. Oben auf GitHub **Code → Download ZIP** wählen.
2. ZIP auf dem Computer entpacken.
3. Den Ordner in Codex oder Claude Code öffnen.
4. Den Masterprompt-Link einfügen.
5. Der Agent prüft das Gerät, erstellt Sicherungen und bereitet die passende
   Änderung vor. Nur bei passenden Voraussetzungen folgt ein begrenzter Test.
6. Dock, App → Home und Wiederherstellung prüfen; erst danach übernehmen.

Alle Details mit Rückweg stehen in [START-HERE.md](START-HERE.md).
Keine fremde TV-Firmware herunterladen und keine undokumentierten Service-
Menü-Werte übernehmen.

Design-Quelle: **[Libraries.dev](https://libraries.dev/)**, insbesondere Liquid
Metal / metal-fx. Auf dem TV wird der Effekt mit kleinen vorberechneten Bildern
dargestellt. [Weitere Credits und Lizenzen](CREDITS.md).

## Nichtkommerzielle Nutzung

Neue eigene Beiträge des Maintainers stehen unter
[PolyForm Noncommercial 1.0.0](LICENSE). Privat nutzen und als Hobby anpassen ist
erlaubt; kommerzielle Nutzung dieser Beiträge braucht eine separate Erlaubnis.
Fremder MIT-Code und bereits unter MIT veröffentlichte Versionen behalten ihre
bisherigen Rechte. Die [Lizenzabgrenzung](LICENSE-SCOPE.md) erklärt die Details.
