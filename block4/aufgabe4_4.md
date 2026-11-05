# Auftrag 4.4: Kubernetes mit minikube (Installation)

Ziel: minikube, kubectl und oc im Ubuntu WSL installieren und einen lokalen Kubernetes-Cluster starten.

## Was sind die Tools?

| Tool | Wofür |
|------|-------|
| **minikube** | Startet einen ganzen Kubernetes-Cluster lokal (ein einziger Node, läuft hier als Docker-Container). Nur zum Lernen und Testen |
| **kubectl** | CLI, um mit jedem Kubernetes-Cluster zu reden (Pods, Deployments, Services erstellen und anschauen) |
| **oc** | CLI für OpenShift (Kubernetes von Red Hat), braucht man später für APPUiO in Block 6 |

## Basis-Abhängigkeiten

```bash
sudo apt update
sudo apt install -y curl
```

## minikube installieren

```bash
sudo curl -Lo /usr/local/bin/minikube https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo chmod +x /usr/local/bin/minikube
echo 'source <(minikube completion bash)' >>~/.bashrc
```

## kubectl installieren

```bash
version=$(curl -sL https://dl.k8s.io/release/stable.txt)
sudo curl -Lo /usr/local/bin/kubectl https://dl.k8s.io/release/$version/bin/linux/amd64/kubectl
sudo chmod +x /usr/local/bin/kubectl
echo 'source <(kubectl completion bash)' >>~/.bashrc
echo 'alias k=kubectl' >>~/.bashrc
echo 'complete -o default -F __start_kubectl k' >>~/.bashrc
```

- Die URL aus der Anleitung (`storage.googleapis.com/kubernetes-release`) wird nicht mehr aktualisiert und liefert nur v1.31.0
- `dl.k8s.io` ist die offizielle Quelle und liefert die aktuelle Version
- kubectl sollte höchstens eine Minor-Version vom Cluster abweichen

## oc installieren

```bash
curl -s https://downloads-openshift-console.apps.exoscale-ch-gva-2-0.appuio.cloud/amd64/linux/oc.tar | sudo tar xvf - --exclude="*.md" -C /usr/local/bin/
echo 'source <(oc completion bash)' >>~/.bashrc
```

## Kontrolle

```bash
source ~/.bashrc
minikube version
kubectl version --client
oc version --client
```

## Start und Konfiguration

```bash
minikube start --driver=docker

minikube addons enable ingress
minikube addons enable dashboard
minikube addons enable metrics-server

minikube dashboard --url
```

- `--driver=docker` minikube läuft als Container in Docker, keine eigene VM nötig
- `minikube start` setzt auch automatisch den kubectl Kontext auf `minikube`

## Add-ons

| Add-on | Wofür |
|--------|-------|
| **ingress** | Nginx Ingress Controller, leitet HTTP-Anfragen von aussen anhand von Hostname/Pfad an die richtigen Services weiter |
| **dashboard** | Web-Oberfläche, um den Cluster grafisch anzuschauen (Pods, Deployments, Logs) |
| **metrics-server** | Sammelt CPU- und RAM-Verbrauch der Pods, nötig für `kubectl top` und Autoscaling |

## Test, ob der Cluster läuft

```bash
minikube status
kubectl get nodes
kubectl get pods -A
```

- `kubectl get nodes` zeigt einen Node `minikube` mit Status `Ready`
- `kubectl get pods -A` zeigt die System-Pods (coredns, etcd, kube-apiserver, ingress, dashboard, metrics-server)

## Nach jedem Neustart

```bash
minikube start --driver=docker
minikube dashboard --url
```

## Nützliche Befehle

| Befehl | Wirkung |
|--------|---------|
| `minikube stop` | Cluster anhalten, alles bleibt erhalten |
| `minikube delete` | Cluster komplett löschen |
| `minikube ip` | IP vom Node |
| `minikube addons list` | Alle Add-ons und ob sie aktiv sind |
| `kubectl top pods -A` | Ressourcenverbrauch (braucht metrics-server) |
