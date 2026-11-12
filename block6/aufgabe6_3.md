# Auftrag 6.3: HTML-Seite auf OpenShift deployen

Ziel: die HTML-Seite aus Auftrag 3.4 als Container auf OpenShift (APPUiO) laufen lassen, mit `nginx-unprivileged` statt dem normalen nginx.

## Struktur

```
aufgabe6_3/
  index.html        HTML-Seite aus 3.4
  Dockerfile        nginx-unprivileged + index.html
  deployment.yml    Deployment: 1 Pod mit dem Image aus ghcr.io
  service.yml       Service: interner Zugriff auf Port 8080
  route.yml         Route: öffentliche HTTPS-Adresse
```

## Warum nginx-unprivileged?

- Das normale `nginx` Image startet als **root** und hört auf Port **80**
- OpenShift lässt Container aus Sicherheitsgründen **nicht als root** laufen, und Ports unter 1024 brauchen root
- `nginxinc/nginx-unprivileged` läuft als normaler User (`nginx`, uid 101) und hört auf Port **8080**
- Darum ist überall Port 8080 statt 80

## Dockerfile

```dockerfile
FROM nginxinc/nginx-unprivileged:latest
COPY index.html /usr/share/nginx/html/index.html
```

## Lokal builden und testen

```bash
cd block6/aufgabe6_3
docker build -t ghcr.io/elyesghazel/html-openshift-app:v1 .
docker run -d --rm -p 8080:8080 --name html-test ghcr.io/elyesghazel/html-openshift-app:v1
curl localhost:8080
docker stop html-test
```

- Im Browser `http://localhost:8080` zeigt die Seite aus 3.4

## In die GitHub Container Registry pushen

```bash
docker login ghcr.io -u elyesghazel
docker push ghcr.io/elyesghazel/html-openshift-app:v1
```

- Zum **Pushen** braucht der PAT die Berechtigung `write:packages` (der Token aus 6.2 hat nur `read:packages`)
- Das Paket ist danach unter github.com/elyesghazel?tab=packages sichtbar und standardmässig **privat**
- OpenShift kann es trotzdem holen, weil in 6.2 das Secret `ghcr` mit dem Service Account `default` verknüpft wurde

## Die drei Dateien

### deployment.yml

- Startet 1 Pod (`replicas: 1`) mit dem Image `ghcr.io/elyesghazel/html-openshift-app:v1`
- `imagePullPolicy: Always` holt das Image bei jedem Start neu aus der Registry
- Das Label `app: web-app` verbindet Deployment, Pods und Service
- `app.kubernetes.io/part-of: web-app` gruppiert alles in der Topologie-Ansicht der Web Console

### service.yml

- Interner Service `web-app-svc` (Typ ClusterIP), leitet Port 8080 an Port 8080 vom Pod weiter
- Findet den Pod über `selector: app: web-app`

### route.yml

- Gibt es nur bei **OpenShift**, nicht bei normalem Kubernetes (dort wäre es ein Ingress)
- Erstellt eine öffentliche Adresse und leitet sie an den Service weiter
- `termination: edge` HTTPS endet beim OpenShift Router, das Zertifikat kommt von OpenShift
- `insecureEdgeTerminationPolicy: Redirect` HTTP wird automatisch auf HTTPS umgeleitet

## Deployment

```bash
oc project <kursnummer>-<kürzel>
oc apply -f deployment.yml
oc apply -f service.yml
oc apply -f route.yml
```

Oder alles auf einmal:

```bash
oc apply -f .
```

## Kontrolle

```bash
oc get pods
oc get svc
oc get routes
```

- Der Pod muss `Running` und `1/1` sein
- Bei `oc get routes` steht unter HOST/PORT die Adresse, im Browser mit `https://` öffnen

| Fehler | Ursache |
|--------|---------|
| `ErrImagePull` / `ImagePullBackOff` | Image-Name falsch, Image nicht gepusht oder Secret `ghcr` fehlt bzw. ist nicht verknüpft |
| `CrashLoopBackOff` | Normales `nginx` statt `nginx-unprivileged` verwendet |
| Route zeigt "Application is not available" | Pod läuft nicht oder Port im Service stimmt nicht |

Bei mir kam zuerst `ErrImagePull`, weil das Secret `ghcr` nicht mit dem Service Account verknüpft war. Lösung:

```bash
oc secrets link default ghcr --for=pull
oc rollout restart deployment/web-app
```

## Update der Seite (manuell)

```bash
# index.html ändern, dann:
docker build -t ghcr.io/elyesghazel/html-openshift-app:v2 .
docker push ghcr.io/elyesghazel/html-openshift-app:v2
# Tag in deployment.yml auf v2 ändern
oc apply -f deployment.yml
```

- Wenn der Tag gleich bleibt (z.B. `:latest`), reicht nach dem Push `oc rollout restart deployment/web-app`
- Das funktioniert nur wegen `imagePullPolicy: Always`, sonst nimmt OpenShift das alte Image aus dem Cache

## Denkanstoss: Vorteile von Continuous Deployment

- **Weniger Fehler**: kein vergessener Build, falscher Tag oder vergessenes `rollout restart`
- **Schneller**: ein `git push` reicht, die Änderung ist nach wenigen Minuten online
- **Nachvollziehbar**: jede Version gehört zu einem Commit, man sieht wer was wann deployt hat
- **Einfacher Rollback**: alten Commit bzw. alten Image-Tag wieder deployen
- **Immer gleich**: die Pipeline macht jedes Mal genau die gleichen Schritte, egal wer pusht
- **Tests vor dem Deployment**: die Pipeline kann zuerst testen und nur bei Erfolg deployen
- **Keine Zugangsdaten auf den Laptops**: Token für Registry und OpenShift liegen nur als Secrets in der Pipeline

## Aufräumen

```bash
oc delete -f .
```
