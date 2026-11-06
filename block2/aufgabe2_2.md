# Auftrag 2.2: Git und Versionsverwaltung (Zusammenfassung)

## Warum Versionsverwaltung?

- Man sieht, **wer was wann warum** geändert hat
- Man kann zu jedem früheren Stand zurück
- Mehrere Personen können gleichzeitig am gleichen Projekt arbeiten

## Die vier Bereiche

```
Arbeitsverzeichnis  --git add-->  Staging  --git commit-->  Lokales Repo  --git push-->  Remote (GitHub)
                                                            Lokales Repo  <--git pull--  Remote
```

## Basis Workflow

| Schritt | Befehl | Bedeutung |
|---------|--------|-----------|
| 1. Start | `git init` | Neues Repo im aktuellen Ordner erstellen |
| | `git clone <url>` | Vorhandenes Projekt vom Server kopieren |
| 2. Vorbereiten | `git status` | Zeigt geänderte Dateien |
| | `git add <datei>` / `git add .` | Datei bzw. alle Änderungen für den nächsten Commit vormerken |
| 3. Speichern | `git commit -m "Nachricht"` | Änderungen **lokal** als neue Version speichern |
| 4. Synchronisieren | `git push` | Eigene Commits auf den Server hochladen |
| | `git pull` | Änderungen vom Server holen und mergen |

## Branching

- Ein Branch ist ein eigener Entwicklungszweig, der `main` bleibt stabil

```bash
git branch                  # alle Branches anzeigen
git switch -c feature-abc   # Branch erstellen und direkt wechseln
git switch main             # zurück zum Hauptbranch
git merge feature-abc       # Arbeit aus feature-abc in den aktuellen Branch übernehmen
```

## Remote

```bash
git remote -v                         # verknüpfte Server-URLs anzeigen
git remote add origin <url>           # lokales Repo mit dem Server verknüpfen
git push -u origin main               # main hochladen und Verknüpfung (Upstream) setzen
```

- Nach `-u` reicht in Zukunft ein einfaches `git push`

## .gitignore

- Dateien, die nicht ins Repo gehören

```
node_modules/   # ganze Ordner
*.log           # alle Logdateien
.env            # Umgebungsvariablen mit Passwörtern
```

## CI/CD

- Bei jedem Push automatisch testen, bauen und deployen
- **GitHub Actions**: `.github/workflows/main.yml`
- **GitLab CI**: `.gitlab-ci.yml` im Root vom Repo

## Tipp

- [Learn Git Branching](https://learngitbranching.js.org/) zeigt grafisch, was bei Branches, Merge und Push passiert
