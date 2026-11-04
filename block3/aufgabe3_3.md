# Auftrag 3.3: Grundlagen Container-Technologie

Beantworten Sie folgende Fragen in der Gruppe und notieren Sie Ihre Antworten stichwortartig.

## Was ist Container-Technologie bzw. Container-Virtualisierung?

- Virtualisierung auf Ebene des Betriebssystems
- Anwendung wird mit allen Abhängigkeiten (Libraries, Laufzeit, Konfiguration) in ein Paket verpackt
- Alle Container teilen sich den **Kernel des Host-OS**, es gibt kein eigenes Gast-OS
- Isolation über Linux Kernel Funktionen:
  - **Namespaces:** jeder Container sieht nur seine eigenen Prozesse, Netzwerk, Dateisystem
  - **cgroups:** begrenzen CPU, RAM, I/O pro Container
- Ziel: Anwendung läuft überall gleich ("works on my machine" Problem gelöst)

## Was sind die Vor- und Nachteile von Containern gegenüber virtuellen Servern (VMs)?

**Vorteile**
- Sehr schnell gestartet (Sekunden statt Minuten)
- Wenig Speicherbedarf (MB statt GB), kein eigenes OS
- Viel mehr Container als VMs auf derselben Hardware
- Portabel: gleiches Image auf Laptop, Server und in der Cloud
- Ideal für Microservices, CI/CD und Skalierung

**Nachteile**
- Schwächere Isolation, da alle den gleichen Kernel teilen (Sicherheitsrisiko bei Kernel-Lücken)
- Nur gleiches OS wie der Host (Linux Container brauchen einen Linux Kernel)
- Daten gehen ohne Volume beim Löschen verloren
- Komplexer bei vielen Containern (braucht Orchestrierung, z.B. Kubernetes)
- Nicht geeignet für Anwendungen, die ein eigenes OS oder Kernel-Zugriff brauchen

## Welche Produkte/Technologien kennen Sie im Umfeld von VMs und Containern?

**VMs / Hypervisor**
- Typ 1 (direkt auf Hardware): VMware ESXi, Microsoft Hyper-V, KVM, Proxmox, Xen
- Typ 2 (auf einem OS): VirtualBox, VMware Workstation, Parallels

**Container**
- Docker, Podman, containerd, CRI-O, LXC/LXD

**Orchestrierung**
- Kubernetes, OpenShift (APPUiO), Docker Swarm, Docker Compose, Minikube

**Cloud**
- AWS ECS/EKS, Azure AKS, Google GKE / Cloud Run

## Wie unterscheiden sich VM und Container hinsichtlich Bereitstellung, Speicherbedarf, Portabilität, Effizienz und OS-Kernel?

| Kriterium | VM | Container |
|---|---|---|
| Bereitstellung | Minuten, ganzes OS muss booten | Sekunden, nur der Prozess startet |
| Speicherbedarf | GB (komplettes Gast-OS) | MB (nur App und Abhängigkeiten) |
| Portabilität | Image gross, an Hypervisor gebunden | Image klein, läuft überall wo eine Container Engine ist |
| Effizienz | Overhead durch Gast-OS, weniger VMs pro Host | kaum Overhead, viele Container pro Host |
| OS-Kernel | jede VM hat einen eigenen Kernel | alle Container teilen den Kernel vom Host |

**Skizze: Architektur**

```
        VM                                  Container
+---------+---------+               +---------+---------+
|  App A  |  App B  |               |  App A  |  App B  |
+---------+---------+               +---------+---------+
| Libs    | Libs    |               | Libs    | Libs    |
+---------+---------+               +---------+---------+
| Gast-OS | Gast-OS |               |  Container Engine |  <- Docker
+---------+---------+               +-------------------+
|    Hypervisor     |  <- hier      |      Host-OS      |
+-------------------+               |   (ein Kernel)    |
|  Host-OS (Typ 2)  |               +-------------------+
+-------------------+               |     Hardware      |
|     Hardware      |               +-------------------+
+-------------------+
```

- **VM:** Hypervisor liegt zwischen Hardware (bzw. Host-OS) und den Gast-Betriebssystemen
- **Container:** Container Engine liegt auf dem Host-OS, darüber direkt die Apps, kein Gast-OS

## Können virtuelle Server immer durch Container ersetzt werden? Begründen Sie.

- **Nein**
- Container brauchen den gleichen Kernel wie der Host (z.B. Windows App auf Linux Host geht nicht)
- Anwendungen mit eigenem Kernel, Kernel-Modulen oder speziellen Treibern brauchen eine VM
- Ältere monolithische Anwendungen sind oft nicht für Container gebaut
- Wenn starke Isolation nötig ist (Sicherheit, verschiedene Kunden), sind VMs besser
- In der Praxis oft kombiniert: Container laufen **in** VMs (z.B. Kubernetes Nodes in der Cloud sind VMs)

## Können Sie die Begriffe Container, Image und Registry erläutern?

- **Image:** unveränderbare Vorlage (Bauplan) mit App, Libraries und Konfiguration, besteht aus mehreren Schichten (Layers)
- **Container:** laufende Instanz eines Images, ein Image kann viele Container starten (wie Klasse und Objekt)
- **Registry:** Speicher für Images, von dort werden sie gepusht und gepullt (z.B. Docker Hub, GHCR, GitLab Registry, AWS ECR)

## Dockerfile: Welche Rolle spielt das Dockerfile im Build-Prozess und wie führt es Applikationscode, Basis-Betriebssystem und Laufzeitumgebung zusammen?

- Das Dockerfile ist das **Rezept** für ein Image, `docker build` führt es Schritt für Schritt aus
- Jede Anweisung erzeugt einen neuen **Layer**, unveränderte Layers werden aus dem Cache genommen (schneller Build)
- So kommen die drei Teile zusammen:
  - **Basis-OS:** `FROM` wählt das Basis-Image (z.B. `ubuntu`, `alpine`)
  - **Laufzeitumgebung:** Basis-Image mit Runtime (z.B. `python:3.12`) oder Installation mit `RUN`
  - **Applikationscode:** `COPY` kopiert den Code ins Image, `CMD` legt fest, was beim Start läuft

```dockerfile
FROM python:3.12-slim                 # Basis-OS + Laufzeitumgebung
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt   # Abhängigkeiten
COPY . .                              # Applikationscode
EXPOSE 8000
CMD ["python", "app.py"]              # Startbefehl
```

## Container Runtimes: Welche Container-Engines oder Runtimes kennen Sie?

- **Engines (High-Level):** Docker Engine, Podman, containerd, CRI-O
- **Low-Level Runtimes:** runc (Standard), crun, gVisor (mehr Isolation), Kata Containers (Container in leichter VM)
- Standard dafür: **OCI** (Open Container Initiative), darum laufen Images auf allen Engines

## Weshalb werden laufende Container in der Praxis als unveränderbar (immutable) betrachtet?

- Man ändert einen laufenden Container nicht, sondern baut ein **neues Image** und ersetzt den Container
- Änderungen im Container landen nur in einer dünnen, beschreibbaren Schicht
  - Nach einem Neustart (`docker restart`) sind sie noch da
  - Wird der Container gelöscht und neu erstellt (normal bei Updates), sind sie **weg**
- Vorteile:
  - Gleicher Zustand in Test und Produktion, reproduzierbar
  - Einfaches Rollback auf die alte Image-Version
  - Keine "vergessenen" manuellen Änderungen
- Daten, die bleiben müssen, gehören in ein **Volume** oder eine Datenbank

## Was ist der Unterschied zwischen Self-Managed und Fully Managed (Cloud-Services)?

- **Self-Managed:** man betreibt alles selbst (z.B. Kubernetes oder Datenbank auf eigenen VMs)
  - volle Kontrolle und Konfiguration
  - aber selbst verantwortlich für Updates, Patches, Backups, Skalierung, Ausfälle
- **Fully Managed:** der Cloud-Anbieter betreibt den Dienst (z.B. AWS RDS, Azure AKS, Google Cloud Run)
  - weniger Aufwand, Anbieter macht Updates, Backups, Hochverfügbarkeit
  - aber weniger Kontrolle, oft teurer, Abhängigkeit vom Anbieter (Lock-in)
- Zusammenhang mit Shared Responsibility: je mehr managed, desto mehr Verantwortung beim Anbieter
