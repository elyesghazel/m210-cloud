# Auftrag 4.1: Container-Orchestrierung

Besprechen Sie in der Gruppe die folgenden Fragen. Dokumentieren Sie Ihre Ergebnisse stichwortartig.

## Warum braucht man Container-Orchestrierung?

- Bei vielen Containern auf mehreren Servern geht es von Hand nicht mehr
- Der Orchestrator übernimmt:
  - Provisionierung und Deployment
  - Konfiguration und Planung (auf welchem Node läuft welcher Container)
  - Ressourcenzuweisung (CPU, RAM)
  - Verfügbarkeit: abgestürzte Container automatisch neu starten
  - Skalieren oder Entfernen von Containern
  - Load Balancing und Traffic Routing
  - Überwachen der Container
  - Konfigurieren von Anwendungen
  - Sichern der Kommunikation zwischen Containern
- Er muss wissen, welches Image er von welcher Registry holen soll und auf welchem Node er den Container startet

## Wie funktioniert Container-Orchestrierung?

- **Konfiguration:** der Soll-Zustand wird in YAML oder JSON beschrieben (Image, Anzahl Instanzen, Ports)
- **Deployment:** der Orchestrator wählt einen passenden Node und startet dort den Container
- **Lifecycle:** Ist-Zustand und Soll-Zustand werden laufend abgeglichen: Container neu starten, verschieben, skalieren
- **Umgebung:** funktioniert überall, wo Container laufen: lokal, Private Cloud oder Public Cloud
- Deklarativ: man sagt **was** man will, nicht wie

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
spec:
  replicas: 3            # Soll-Zustand: 3 Instanzen
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
        - name: web
          image: ghcr.io/elyesghazel/web:1.0
          ports:
            - containerPort: 8080
```

- Stürzt einer der 3 Pods ab, startet Kubernetes automatisch einen neuen

## Welche Container-Orchestrierung Technologien kennen Sie?

**Orchestratoren**
- Kubernetes (Standard)
- Managed Kubernetes in der Cloud: Amazon EKS, Azure AKS, Google GKE
- Red Hat OpenShift (z.B. APPUiO)
- K3s (leichtes Kubernetes)
- Docker Swarm
- HashiCorp Nomad
- Lokal / zum Lernen: Docker Compose (ein Host), Minikube

**Ökosystem rund um Kubernetes (keine Orchestratoren)**
- Rancher: Cluster-Verwaltung
- Helm: Paketmanager
- Argo CD: GitOps / Continuous Deployment
- Tekton: CI/CD-Pipelines

## Was versteht man unter horizontaler Skalierung im Kontext von Cloud-Anwendungen?

- **Horizontal (Scale out):** mehr identische Instanzen (Pods) starten, z.B. `replicas` von 1 auf 3
  - Der Service verteilt die Anfragen auf alle Pods (Load Balancing)
  - Setzt zustandslose Anwendungen voraus (12 Factor, Faktor 6)
  - In Sekunden möglich
  - Automatisch mit dem **Horizontal Pod Autoscaler (HPA)**: min. und max. Anzahl Pods und Ziel-Auslastung festlegen (z.B. 70% CPU)
- Im Gegensatz dazu **vertikal (Scale up):** derselbe Pod bekommt mehr CPU und RAM
  - Anzahl Pods bleibt gleich, automatisch mit dem Vertical Pod Autoscaler (VPA)
  - Für zustandsbehaftete Anwendungen
  - Grenze: ein Pod kann nie grösser werden als der Node

## Was gibt es für Deployment Strategien?

| Strategie | Ablauf | Vorteil | Nachteil |
|---|---|---|---|
| **Recreate** | Alle alten Pods beenden, dann neue starten | Einfach, keine zusätzlichen Ressourcen, v1 und v2 laufen nie gleichzeitig | Ausfallzeit |
| **Blue/Green** | Neue Version (Green) läuft parallel zur alten (Blue), Traffic wird auf einmal umgeschaltet (z.B. Service-Selector ändern) | Neue Version vorher testbar, schnelles Rollback solange Blue läuft | Doppelte Ressourcen während der Umstellung |
| **Rolling Update** | Pods werden schrittweise ersetzt | Keine Ausfallzeit, kaum zusätzliche Ressourcen, Standard in Kubernetes (`RollingUpdate`) | Dauert länger, v1 und v2 beantworten kurz gleichzeitig Anfragen |
| **Canary** | Neue Version bekommt zuerst nur einen kleinen Teil des Traffics (z.B. 10%), dann schrittweise mehr | Geringes Risiko, schnelles Rollback, günstiger als Blue/Green | Braucht gutes Monitoring, App und DB müssen beide Versionen unterstützen |

- Recreate ist sinnvoll, wenn v1 und v2 nie gleichzeitig laufen dürfen (z.B. inkompatibles DB-Schema)
