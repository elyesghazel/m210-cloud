# Auftrag 3.2: Docker-Workflow & Kommandos

Theorie-Block: die wichtigsten Befehle für den Lebenszyklus eines Containers.

## 1. Authentifizierung an der Registry

- Vor dem Pushen muss man sich bei der Registry anmelden
- Dafür braucht es ein **Personal Access Token (PAT)**
  - GitHub: Berechtigung `write:packages`
  - GitLab: Berechtigung `api`
  - Ohne diese Berechtigung gibt es beim Push "Permission Denied"

```bash
# GitHub Container Registry (GHCR)
echo $GITHUB_TOKEN | docker login ghcr.io -u githubusername --password-stdin

# GitLab Container Registry
echo $GITLAB_TOKEN | docker login registry.gitlab.com -u gitlabusername --password-stdin
```

- `--password-stdin`: Token kommt über die Pipe, nicht als Argument (landet nicht in der History)

## 2. Docker Workflow: Bauen, Testen, Publizieren

```bash
# 1. Image bauen
#    -f = Pfad zum Dockerfile, -t = Tag (Name:Version), . = aktuelles Verzeichnis (Build-Kontext)
docker build -f Dockerfile.app -t ghcr.io/githubusername/mein-image:v1 .

# 2. Lokal testen
#    -d = im Hintergrund, -p 8080:80 = Port 8080 vom Host auf Port 80 im Container
docker run -d -p 8080:80 --name meincontainername ghcr.io/githubusername/mein-image:v1

# 3. Mit Persistenz testen (Volume-Mount)
#    -v = Ordner vom Host in den Container einbinden, Daten bleiben nach dem Löschen des Containers
docker run -d -p 8080:80 --name meincontainername -v "${PWD}/daten:/app/daten" ghcr.io/githubusername/mein-image:v1

# 4. In die Registry hochladen
docker push ghcr.io/githubusername/mein-image:v1
```

- Reihenfolge: **build** > **run** (testen) > **push**
- Der Tag enthält die Registry: `ghcr.io/benutzer/image:version`

## 3. Verwaltung von Containern & Images

| Befehl | Erklärung |
|---|---|
| `docker ps` | Listet alle laufenden Container auf |
| `docker ps -a` | Listet alle Container auf (auch gestoppte) |
| `docker stop [name/id]` | Stoppt einen laufenden Container sauber |
| `docker rm [name/id]` | Löscht einen (gestoppten) Container endgültig |
| `docker exec -it [name] /bin/bash` (oder `/bin/sh`) | Öffnet eine interaktive Shell im laufenden Container |
| `docker images` | Zeigt alle lokalen Images an |
| `docker rmi [image]` | Löscht ein lokales Image |
| `docker system prune -a` | Löscht alle ungenutzten Ressourcen (Container, Images, Netzwerke) |

## Wichtig

- Bei einer anderen Registry als Docker Hub immer den vollen Pfad angeben: `docker push registry.example.com/benutzer/image:tag`
- Vorher mit `docker login [URL]` anmelden
- Mein Login: `docker login ghcr.io -u elyesghazel` hat funktioniert (Login Succeeded)
