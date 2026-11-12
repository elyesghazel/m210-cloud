# Auftrag 6.4: APPUiO Tech Labs

Pflichtübungen aus den [APPUiO Tech Labs](https://github.com/appuio/techlab/tree/lab-4): Lab 04 (Docker Image deployen), Lab 05 (Route erstellen) und Lab 06 (Skalieren).

## Lab 04: Container Image deployen

```bash
oc new-project 264830-elygha-dockerimage
oc new-app quay.io/appuio/example-spring-boot --as-deployment-config
oc get pods -w
oc status
oc get all
```

- `oc new-app` erstellt alles selber, ohne eigene YAML-Dateien (in 6.3 habe ich die YAML-Dateien noch selber geschrieben)
- `--as-deployment-config` erstellt eine DeploymentConfig statt einem Deployment, die Labs bauen darauf auf. Gibt eine Warnung, weil DeploymentConfig ab OpenShift 4.14 veraltet ist

### Was `oc new-app` erstellt hat

| Ressource | Aufgabe |
|-----------|---------|
| **DeploymentConfig** | Beschreibt, welches Image mit wie vielen Pods laufen soll und wann neu deployt wird (Trigger `config` und `image`) |
| **ReplicationController** | Wird von der DeploymentConfig erstellt, sorgt dafür, dass immer genau die gewünschte Anzahl Pods läuft |
| **Pod** | Der laufende Container. Dazu kommt ein `-deploy` Pod, der nur das Rollout macht und danach `Completed` ist |
| **Service** | Interne feste IP (ClusterIP), verteilt die Anfragen auf die Pods |
| **ImageStream** | Zeigt auf das Image in der internen APPUiO Registry. Wenn sich das Image ändert, startet automatisch ein neues Deployment |

### Service und Pod verbinden

```bash
oc describe svc example-spring-boot
```

- `Selector: deploymentconfig=example-spring-boot` sucht alle Pods mit diesem Label
- Unter `Endpoints` steht die IP vom gefundenen Pod (bei mir `10.0.6.194:8080`)
- Die Service IP bleibt immer gleich, die Pod IP ändert sich bei jedem neuen Pod
- Die Fehlermeldung `ciliumconfigs.cilium.io is forbidden` bei `oc get all` kann man ignorieren, als normaler User darf man diese Cluster-Objekte nicht sehen

## Lab 05: Routen erstellen

```bash
oc expose service example-spring-boot
oc create route edge example-spring-boot-secure --service=example-spring-boot
oc get routes
```

| Route | Adresse |
|-------|---------|
| `example-spring-boot` | `http://example-spring-boot-264830-elygha-dockerimage.apps.exoscale-ch-gva-2-0.appuio.cloud` |
| `example-spring-boot-secure` | `https://example-spring-boot-secure-264830-elygha-dockerimage.apps.exoscale-ch-gva-2-0.appuio.cloud` |

- `oc expose` macht eine unverschlüsselte Route (HTTP)
- `oc create route edge` macht eine HTTPS Route, das Zertifikat kommt vom OpenShift Router
- Ohne eigenen Hostname wird die Adresse aus Service-Name, Projekt und Cluster-Domain gebildet
- Der Router entscheidet anhand vom Hostname, an welchen Service eine Anfrage geht
- Danach im Browser ein paar "Say Hello" Einträge gemacht

## Lab 06: Skalieren, Readiness Probe und Self Healing

### App deployen und skalieren

```bash
oc new-project 264830-elygha-scale
oc new-app appuio/example-php-docker-helloworld --name=appuio-php-docker --as-deployment-config
oc expose service appuio-php-docker
oc get rc
oc scale --replicas=3 dc/appuio-php-docker
oc get pods
oc describe svc appuio-php-docker
```

- Man skaliert die **DeploymentConfig**, nicht den ReplicationController, die DC gibt die Anzahl an den RC weiter
- Nach dem Skalieren hat der Service 3 Endpoints: `10.0.6.157`, `10.0.10.202`, `10.0.9.33`
- Die IPs sind in verschiedenen Netzen, die Pods laufen also auf verschiedenen Nodes
- In der Web Console (Developer > Topology > App anklicken) kann man die Anzahl Pods mit den Pfeilen neben dem Ring ändern

### Unterbruchsfrei skalieren testen

Im ersten Terminal jede Sekunde eine Anfrage schicken (fish):

```bash
while true; curl -s -m 2 http://appuio-php-docker-264830-elygha-scale.apps.exoscale-ch-gva-2-0.appuio.cloud/pod/; echo " "(date "+%H:%M:%S"); sleep 1; end
```

Im zweiten Terminal:

```bash
oc scale --replicas=1 dc/appuio-php-docker
oc rollout latest appuio-php-docker
```

- Die Antworten kommen abwechselnd von verschiedenen Pods (Load Balancing durch den Service)
- Beim Herunterskalieren gibt es keinen Unterbruch, danach antwortet nur noch ein Pod
- Bei `oc rollout latest` ohne Health Check gibt es eine kurze Lücke, weil der neue Pod schon Traffic bekommt, bevor die App bereit ist

### Readiness Probe

```bash
oc set probe dc/appuio-php-docker --readiness --get-url=http://:8080/health --initial-delay-seconds=10
oc rollout latest appuio-php-docker
```

- OpenShift fragt alle 10 Sekunden `/health` ab, erst bei Status 200 bekommt der Pod Traffic
- Der alte Pod antwortet weiter, bis der neue bereit ist (Rolling Update), darum gibt es jetzt keinen Unterbruch mehr

| Probe | Frage | Wenn sie fehlschlägt |
|-------|-------|----------------------|
| **Readiness** | Ist die App bereit für Anfragen? | Pod bekommt keinen Traffic, läuft aber weiter |
| **Liveness** | Läuft die App noch sauber? | Pod wird neu gestartet |

### Self Healing

```bash
oc get pods -w                                          # Terminal 1
oc delete pods -l deploymentconfig=appuio-php-docker    # Terminal 2
```

- Die gelöschten Pods sind `Terminating`, sofort werden neue erstellt
- Der ReplicationController merkt, dass weniger Pods laufen als gewünscht und startet neue
- Die neuen Pods sind erst `1/1`, wenn die Readiness Probe OK meldet

## Erkenntnisse

- `oc new-app` ist schnell zum Ausprobieren, aber die Konfiguration existiert dann nur im Cluster. Mit YAML-Dateien im Git (wie in 6.3) kann man alles jederzeit wieder aufbauen
- **Route > Service > Pod**, die Verbindung zwischen Service und Pods läuft immer über Labels
- Skalieren geht in Sekunden, weil nur weitere Container vom gleichen Image gestartet werden
- Ohne Readiness Probe kann ein Update kurz zu einem Ausfall führen, mit Probe und Rolling Update nicht
- OpenShift hält den Soll-Zustand selber aufrecht (Self Healing)
