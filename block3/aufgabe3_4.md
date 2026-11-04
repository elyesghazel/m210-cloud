# Auftrag 3.4: Webserver mit Docker

Ziel: einen Webserver mit Docker lokal zum Laufen bringen, einmal mit Volume und einmal mit eigenem Image.

## Struktur

```
aufgabe3_4/
  app/web/index.html
  dockerfiles/Dockerfile.web
```

## HTML-Inhalt erstellen

- Einfache `index.html` in `app/web/`

## Variante A (Direkt): Nginx-Container mit Volume-Mount

```bash
docker run -d -p 8080:80 --name web-vol -v "${PWD}/app/web:/usr/share/nginx/html:ro" nginx
```

- `-v` bindet den Ordner `app/web` vom Host in den Container ein, `:ro` = nur lesen
- Test unter http://localhost:8080
- Änderungen an der `index.html` sind nach einem Reload sofort sichtbar, ohne Neustart

## Variante B (Image-Build): eigenes Image mit COPY

```dockerfile
FROM nginx:alpine
COPY app/web /usr/share/nginx/html
```

```bash
docker build -f dockerfiles/Dockerfile.web -t mein-webserver .
docker run -d -p 8081:80 --name web-build mein-webserver
```

- Die `index.html` wird beim Build ins Image kopiert
- Test unter http://localhost:8081
- Änderungen an der `index.html` sind erst nach neuem `docker build` und neuem Container sichtbar

## Aufräumen

```bash
docker stop web-vol web-build
docker rm web-vol web-build
```

## Reflexion: Welcher Ansatz ist besser für die Produktion geeignet?

- **Variante B (Image-Build)**
  - Image enthält alles, läuft auf jedem Server gleich (keine Dateien auf dem Host nötig)
  - Versionierbar mit Tags (`v1`, `v2`), einfaches Rollback
  - Immutable: niemand ändert die Dateien im laufenden Betrieb
  - Kann in eine Registry gepusht und automatisch deployed werden
- **Variante A (Volume)** ist gut für die Entwicklung
  - Änderungen sofort sichtbar, kein Build nötig
  - In der Produktion aber abhängig vom Host-Ordner, nicht portabel

## Denkanstoss CI/CD: Wie müsste eine YAML-Datei aussehen, die bei jedem Push automatisch ein neues Image baut und in die Registry schiebt?

GitHub Actions, Datei `.github/workflows/docker.yml`:

```yaml
name: Docker Build und Push

on:
  push:
    branches: [master]

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
      - name: Code auschecken
        uses: actions/checkout@v4

      - name: Login bei GHCR
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Image bauen und pushen
        uses: docker/build-push-action@v6
        with:
          context: block3/aufgabe3_4
          file: block3/aufgabe3_4/dockerfiles/Dockerfile.web
          push: true
          tags: |
            ghcr.io/elyesghazel/mein-webserver:latest
            ghcr.io/elyesghazel/mein-webserver:${{ github.sha }}
```

- `on: push`: startet bei jedem Push auf `master`
- `permissions: packages: write`: erlaubt das Pushen in die GitHub Registry
- `secrets.GITHUB_TOKEN`: Token wird von GitHub automatisch bereitgestellt, kein eigener PAT nötig
- Tag mit `github.sha` (Commit-Hash): jede Version ist eindeutig, `latest` zeigt auf die neueste
- Bei GitLab gleiches Prinzip mit `.gitlab-ci.yml` (`docker build` und `docker push` im `script`)
