# HISinOne QIS - Parser für Prüfungsleistungen

Basiert auf dem Repository: [https://github.com/MrKrisKrisu/HISinOne-QIS-exam-notification](https://github.com/MrKrisKrisu/HISinOne-QIS-exam-notification)

Dieses Script wurde auf die HISinOne Instanz der **Hochschule Fulda** (horstl) angepasst und wird vermutlich für keine andere Hochschule funktionieren.

## Was ist das?
Ein Python Script, das sich für dich in iCMS einloggt und schaut, ob sich Änderungen (zum Beispiel eine neue eingetragene Note) in der Prüfungsübersicht bei dir ergeben haben.

Falls gewünscht benachrichtigt dich das Script dann direkt per Telegram oder E-Mail.

Optional können alle Noten als JSON Datenstruktur oder nur die Änderungen als Text auf der Konsole ausgegeben werden.

Es ist also dafür gedacht, beispielsweise alle 30 Minuten ausgeführt zu werden.
 
> Tut dem Hochschulserver einen Gefallen und fragt **nicht** alle 10 Sekunden ab!
 
## Installationsanleitung
### Telegram einrichten
#### Telegram Bot erstellen
Erstelle über den [BotFather](https://t.me/botfather) einen neuen Bot und schreibe dir den Token heraus.
Mehr Informationen zum erstellen von Telegram Bots: [https://core.telegram.org/bots](https://core.telegram.org/bots)

#### Telegram Chat ID herausfinden
* Erstelle eine neue Gruppe und füge deinen Bot hinzu, sowie den [TelegramRawBot](https://t.me/RawDataBot)
* Schreibe nun eine Nachricht in die Gruppe, der RawBot wird dir antworten
* Schreibe dir deine ID heraus, die unter **message -> from -> id** steht

### Python Umgebung
Die Module requests und lxml sind standardmäßig nicht installiert. Diese können mit pip nachinstalliert werden:
> pip install -r requirements.txt

### Script installieren
- Lade das Script in deine Python Umgebung
- Lass dir mit `python3 crawl.py --config myHisConfig.cfg` eine Konfigurationsdatei erstellen (der Pfad zur Datei kann geändert werden, muss aber schreibbar sin)
- Die Konfigurationsdatei nun manuell anpassen
    - Nutzername und Passwort benötigt (iCMS Zugangsdaten)
    - gerne auch schon mit Telegram oder Mail Support (optional)
- Wenn du das Script jetzt erneut ausführst solltest du einmalig über **alle** eingetragenen Prüfungen benachrichtigt werden.

### Automatisches ausführen
Du kannst dein Script automatisch regelmäßig ausführen lassen (dafür ist es ja auch gedacht). Das kannst du mit einem CronJob realisieren. Erstelle einfach folgenden CronJob:

> */30 * * * * /path/to/crawl.py

Dies führt dein Script automatisch alle 30 Minuten aus. Den Wert kannst du anpassen, aber denk dabei bitte an die armen, armen Hochschulserver! Um das ganze noch mehr einzuschränken kann man die Ausführung auf die prüfungsrelevanten Monate begrenzen:
> */30 * * 1,2,6,7 * /path/to/crawl.py

## Sicherheitshinweis
Du musst dein zentrales Passwort für deinen Hochschulaccount im **Klartext** in der Konfigurationsdatei speichern. Achte daher bitte darauf, dass das Script nur in einer gesicherten Umgebung läuft und durch geeignete Berechtigungen von dem Zugriff Dritter geschützt ist.
