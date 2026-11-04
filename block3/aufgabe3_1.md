# Auftrag 3.1: Installation Docker Desktop

Ziel: lokale Entwicklungsumgebung mit Docker Engine bzw. Docker Desktop einrichten.

## Linux (Ubuntu)

- Nur die native **Docker Engine** verwenden (https://docs.docker.com/engine/install/)
- Benutzer zur Gruppe `docker` hinzufügen, damit Befehle ohne `sudo` laufen:

```bash
sudo usermod -aG docker $USER
# danach neu einloggen
```

## Windows

- Ubuntu WSL aus dem Microsoft Store installieren
- **Docker Desktop** installieren oder updaten
- WSL 2 Integration aktivieren: Docker > Settings > Resources > WSL Integration, Distro einschalten
- Test im Ubuntu Terminal:

```bash
docker ps
```

- Falls `docker` nicht gefunden wird: Distro in WSL Integration aktivieren und Docker Desktop neu starten
- Virtualisierung muss im BIOS/UEFI aktiviert sein, WSL 2 Backend verwenden (bessere Performance)

## Status

- Docker läuft in WSL, `docker ps` funktioniert ohne Fehler
