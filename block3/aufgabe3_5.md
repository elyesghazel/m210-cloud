# Auftrag 3.5: Python-Webserver und Dateiverwaltung in Containern

Ziel: eigene Python-Container erstellen, Sicherheitscheck mit `docker scout`, Unterschied zwischen Build-Zeit (COPY) und Laufzeit (Volumes) verstehen.

## Struktur

```
aufgabe3_5/
  app/python-web/app.py
  app/python-web/requirements.txt
  app/file-reader/app.py
  app/file-reader/data.txt
  app/file-reader/requirements.txt
  dockerfiles/Dockerfile.python-web
  dockerfiles/Dockerfile.file-reader
```

## Vorbereitung: Datei app/file-reader/data.txt erstellen

```bash
echo "Hallo aus der data.txt, Version 1" > app/file-reader/data.txt
```

## Python-Webserver: Flask-App, die einen Namen aus der URL liest und begrüsst

- `app/python-web/app.py` liest den Parameter `name` aus der URL, Standard ist `World`
- Flask läuft auf `0.0.0.0`, damit die App von ausserhalb des Containers erreichbar ist

## Container-Deployment: Dockerfile erstellen, Image bauen, Container starten

```dockerfile
FROM python:3.11-alpine
WORKDIR /app
COPY app/python-web/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/python-web/app.py .
EXPOSE 8080
CMD ["python", "app.py"]
```

```bash
docker build -f dockerfiles/Dockerfile.python-web -t python-web .
docker run -d -p 8080:8080 --name python-web python-web
```

- Test: http://localhost:8080?name=Elyes ergibt `Hello, Elyes!`
- `requirements.txt` wird vor dem Code kopiert: so bleibt der pip Layer im Cache, wenn sich nur der Code ändert

## Sicherheitscheck: docker scout cves, Vergleich mit python:alpine

```bash
docker scout quickview file-reader
docker scout quickview python:3.11
```

| Image | Pakete | Critical | High | Medium | Low | Health Score |
|---|---|---|---|---|---|---|
| eigenes Image (`python:3.11-alpine`) | 78 | 0 | 3 | 6 | 2 | D (50%) |
| `python:3.11` (Debian) | 629 | 2 | 30 | 84 | 248 | D (39%) |

- Alpine Image hat viel weniger Pakete (78 statt 629) und darum viel weniger Schwachstellen
- Weniger Software im Image = kleinere Angriffsfläche
- Scout empfiehlt `python:3.12-alpine` als Update: 2 High, 1 Medium und 1 Low weniger
- Beide Images verletzen die Policy "Image runs as the root user": besser einen eigenen Benutzer anlegen (`USER` im Dockerfile)
- Fazit: kleine Basis-Images (alpine, slim) verwenden und regelmässig aktualisieren

## Dateiverwaltung: zweite Flask-App, die data.txt bei jedem Aufruf ausliest

- `app/file-reader/app.py` öffnet `/data/data.txt` bei jedem Seitenaufruf neu und gibt den Inhalt zurück

## Build vs. Laufzeit: File-Reader als Image, data.txt auf dem Host ändern

```dockerfile
FROM python:3.11-alpine
WORKDIR /app
COPY app/file-reader/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/file-reader/app.py .
COPY app/file-reader/data.txt /data/data.txt
EXPOSE 8080
CMD ["python", "app.py"]
```

```bash
docker build -f dockerfiles/Dockerfile.file-reader -t file-reader .
docker run -d -p 8081:8080 --name file-reader file-reader
echo "Version 2, geaendert auf dem Host" > app/file-reader/data.txt
```

- http://localhost:8081 zeigt weiterhin Version 1
- Die Änderung auf dem Host ist im Container **nicht sichtbar**

## Volumes nutzen: File-Reader mit Bind-Mount starten

```bash
docker stop file-reader && docker rm file-reader
docker run -d -p 8081:8080 --name file-reader -v "${PWD}/app/file-reader/data.txt:/data/data.txt" file-reader
```

- Jetzt zeigt http://localhost:8081 sofort Version 2
- Jede weitere Änderung an der `data.txt` ist nach einem Reload sichtbar, ohne neuen Build
- Die Datei vom Host "überlagert" die Datei aus dem Image

## Fehlersuche: Warum sind Änderungen am Host-File ohne Volume-Mount im Container unsichtbar?

- `COPY` kopiert die Datei beim `docker build` ins Image, sie ist in den **Image-Layer gebrannt**
- Der Container arbeitet mit dieser Kopie, nicht mit der Datei auf dem Host
- Zwischen Host und Container gibt es ohne Volume keine Verbindung
- Für eine neue Version braucht es einen neuen Build und einen neuen Container
- Mit einem Bind-Mount (`-v`) greift der Container direkt auf die Datei vom Host zu

**Merke**
- Build-Zeit (COPY): Code und feste Dateien, gehören ins Image
- Laufzeit (Volume): Daten, die sich ändern oder bleiben müssen
