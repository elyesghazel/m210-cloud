# Auftrag 5.1: Die 12-Factor App

Unsere Gruppe: Faktor **VIII. Concurrency (Nebenläufigkeit)**, Quelle: [12factor.net/de/concurrency](https://12factor.net/de/concurrency)

> Mit dem Prozess-Modell skalieren

## Definition: Um was geht es?

- Jede laufende App besteht aus einem oder mehreren **Prozessen**
- Eine 12-Factor App teilt ihre Arbeit in **Prozesstypen** auf, z.B.
  - **web**: beantwortet HTTP-Anfragen
  - **worker**: erledigt lange Hintergrundarbeiten (Mails versenden, Bilder verkleinern, Reports)
- Mehr Last = **mehr Prozesse starten** (horizontal skalieren), nicht einen Prozess immer grösser machen (vertikal skalieren)
- Die Prozesse teilen nichts untereinander (**share nothing**), darum kann man einfach weitere dazu starten
- Welche Prozesstypen es gibt und wie viele davon laufen heisst **Process Formation**, z.B. 3x web, 2x worker
- Die App startet sich nicht selber im Hintergrund und schreibt keine PID-Dateien, ein **Prozessmanager** kümmert sich um Start, Neustart nach Absturz und Logs

## Motivation: Welches Problem wird gelöst?

| Ohne Faktor VIII | Mit Faktor VIII |
|------------------|-----------------|
| Ein grosser Prozess macht alles | Pro Aufgabe ein eigener Prozesstyp |
| Mehr Last = grösserer Server (mehr CPU, RAM) | Mehr Last = mehr Prozesse auf mehreren Servern |
| Ein Server kann nur bis zu einer Grenze wachsen | Horizontal fast keine Grenze |
| Lange Aufgaben blockieren die Webseite | Worker erledigt sie im Hintergrund, die Webseite bleibt schnell |
| Stürzt der Prozess ab, ist alles weg | Andere Prozesse laufen weiter, der kaputte wird neu gestartet |

- Vertikal skalieren ist teuer und irgendwann am Limit
- Teile der App brauchen unterschiedlich viel Leistung, man will sie **einzeln** skalieren können

## Praxis: Umsetzung in der Cloud

### Docker Compose

```yaml
services:
  web:
    image: meine-app
    command: npm start
  worker:
    image: meine-app
    command: npm run worker
```

```bash
docker compose up -d --scale web=3 --scale worker=2
```

- Gleiches Image, aber zwei Prozesstypen mit anderem Startbefehl

### Kubernetes / OpenShift

- Pro Prozesstyp ein **Deployment** (z.B. `web` und `worker`)
- Anzahl Prozesse = `replicas` im Deployment
- Der **Service** verteilt die Anfragen auf alle web-Pods (Load Balancing)
- Der **ReplicaSet** ist der Prozessmanager: stürzt ein Pod ab, startet er sofort einen neuen

```bash
kubectl scale deployment web --replicas=3
kubectl scale deployment worker --replicas=5
```

- **Autoscaling** (Horizontal Pod Autoscaler): Kubernetes startet automatisch mehr Pods, wenn die CPU-Last hoch ist

```bash
kubectl autoscale deployment web --min=2 --max=10 --cpu-percent=70
```

### Selber ausprobiert (Auftrag 6.4, Lab 06)

```bash
oc scale --replicas=3 dc/appuio-php-docker
oc describe svc appuio-php-docker
```

- Nach wenigen Sekunden 3 Pods, der Service hatte 3 Endpoints auf verschiedenen Nodes
- Die Anfragen wurden abwechselnd von verschiedenen Pods beantwortet
- Pods gelöscht: OpenShift hat sofort neue gestartet

### Weitere Beispiele

- **Heroku**: `Procfile` mit `web:` und `worker:`, skalieren mit `heroku ps:scale web=3`
- **systemd** auf einem normalen Server als Prozessmanager
- Webshop im Black Friday: mehr web-Pods, nach dem Ansturm wieder weniger

## Zusammenhang mit anderen Faktoren

- **VI. Prozesse (stateless)**: nur wenn Prozesse keine Daten lokal speichern, kann man einfach weitere starten
- **IX. Einweggebrauch (Disposability)**: Prozesse müssen schnell starten und sauber stoppen, damit Skalieren schnell geht
- **XI. Logs**: Prozesse schreiben nur nach stdout, der Prozessmanager sammelt die Logs

## Präsentation (max. 5 Minuten)

| Folie | Inhalt | Zeit |
|-------|--------|------|
| 1 | Titel: VIII. Concurrency, "Mit dem Prozess-Modell skalieren" | 0:15 |
| 2 | Definition: Prozesstypen web und worker, Process Formation | 1:00 |
| 3 | Motivation: vertikal vs. horizontal skalieren (Bild: ein grosser Server vs. viele kleine) | 1:00 |
| 4 | Praxis: Kubernetes Deployment mit `replicas`, Service verteilt die Last, Autoscaling | 1:15 |
| 5 | Demo / Screenshot: `oc scale --replicas=3` aus Lab 06 mit 3 Endpoints | 0:45 |
| 6 | Fazit: mehr Last = mehr Prozesse, braucht stateless Prozesse (Faktor VI) | 0:30 |

### Mögliche Fragen aus dem Plenum

- **Was ist der Unterschied zu Threads?** Threads laufen in einem Prozess auf einer Maschine. Faktor VIII erlaubt Threads, aber die App muss zusätzlich über mehrere Prozesse und Maschinen skalieren können
- **Warum keine PID-Dateien / Daemons?** Das ist die Aufgabe vom Prozessmanager (systemd, Kubernetes). Die App läuft einfach im Vordergrund
- **Kann man jede App so skalieren?** Nur wenn sie stateless ist. Speichert eine App Sessions im RAM, landet der Benutzer beim nächsten Request evtl. auf einem anderen Pod und ist ausgeloggt. Lösung: Sessions in Redis oder in der Datenbank
