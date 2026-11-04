# Auftrag 1.2: Grundlagen Cloud-Computing

Beantworten Sie folgende Fragen in der Gruppe und notieren Sie Ihre Antworten stichwortartig.

## Welche Cloud-Dienstleistungen (Servicemodelle) kennen Sie?

- **IaaS (Infrastructure as a Service):** VMs, Speicher, Netzwerk (z.B. AWS EC2, Azure VMs)
- **PaaS (Platform as a Service):** Plattform zum Betreiben eigener Apps (z.B. Heroku, Azure App Service, OpenShift / APPUiO)
- **SaaS (Software as a Service):** fertige Anwendung (z.B. Microsoft 365, Gmail, Salesforce)
- weitere: FaaS / Serverless (z.B. AWS Lambda), CaaS (Container as a Service), DBaaS (z.B. AWS RDS)

## Welche Cloud-Anbieter kennen Sie?

- Amazon Web Services (AWS)
- Microsoft Azure
- Google Cloud Platform (GCP)
- Oracle Cloud, IBM Cloud, Alibaba Cloud
- Schweiz: Swisscom Cloud, Infomaniak, Exoscale, APPUiO (VSHN)

## Was ist der wesentliche Unterschied zwischen Monitoring und Logging in der Cloud?

- **Logging:** Ereignisse werden aufgezeichnet und gespeichert (was ist wann passiert), z.B. Fehlermeldungen, Zugriffe. Wird vor allem im Nachhinein zur Fehlersuche und für Audits gebraucht
- **Monitoring:** laufende Überwachung von Metriken (CPU, RAM, Antwortzeit, Verfügbarkeit). Zeigt den aktuellen Zustand, löst bei Grenzwerten Alarme aus
- Kurz: Logging = Protokoll von Ereignissen, Monitoring = Überwachung des Zustands in Echtzeit

## Weshalb sollte man Dienste aus der Cloud beziehen? Was sind die Vorteile?

- Keine hohen Anfangsinvestitionen in Hardware (OPEX statt CAPEX)
- Pay-per-Use: man zahlt nur, was man braucht
- Schnell skalierbar nach oben und unten
- Ressourcen in Minuten bereit statt Wochen
- Hohe Verfügbarkeit, Rechenzentren an mehreren Standorten
- Anbieter kümmert sich um Hardware, Wartung, Strom, Kühlung
- Zugriff von überall
- Neue Dienste (KI, Datenbanken usw.) einfach nutzbar

## Was sind die entsprechenden Nachteile?

- Abhängigkeit vom Anbieter (Vendor Lock-in)
- Internetverbindung nötig
- Datenschutz: Daten liegen beim Anbieter, evtl. im Ausland (DSG, DSGVO, CLOUD Act)
- Weniger Kontrolle über die Infrastruktur
- Kosten können bei Dauerbetrieb oder falscher Konfiguration hoch werden
- Ausfälle beim Anbieter betreffen viele Kunden gleichzeitig
- Know-how für Konfiguration und Sicherheit nötig

## Was beschreibt das Konzept der "Shared Responsibility" (geteilte Verantwortung) im Kontext der Nutzung von Public-Cloud-Diensten?

- Verantwortung für die Sicherheit ist zwischen Anbieter und Kunde aufgeteilt
- **Anbieter:** Sicherheit DER Cloud (Rechenzentrum, Hardware, Netzwerk, Virtualisierung)
- **Kunde:** Sicherheit IN der Cloud (Daten, Benutzer und Rechte, Konfiguration, Verschlüsselung, eigene Anwendungen)
- Aufteilung hängt vom Servicemodell ab:
  - IaaS: Kunde verantwortet OS, Patches, Firewall, Apps, Daten
  - PaaS: Anbieter verwaltet auch OS und Laufzeitumgebung, Kunde App und Daten
  - SaaS: Anbieter verwaltet fast alles, Kunde bleibt für Daten, Benutzer und Zugriffe verantwortlich
- Daten und Zugriffe sind immer Sache des Kunden

## Infrastruktur als Code (IaC): Welche gängigen Tools existieren, um Cloud-Infrastruktur automatisiert zu definieren und bereitzustellen?

- Terraform / OpenTofu (Standard-Tool, für viele Anbieter)
- AWS CloudFormation
- Azure Resource Manager (ARM Templates) und Bicep
- Pulumi (IaC mit normalen Programmiersprachen)
- Ansible (eher Konfiguration, kann aber auch Ressourcen anlegen)
- Ressourcen werden deklarativ in Dateien beschrieben, das Tool erstellt sie automatisch

## Management-Schnittstellen: Über welche drei grundlegenden Wege kann man eine Cloud-Umgebung verwalten?

- **Webkonsole / Portal im Browser** (z.B. AWS Management Console, Azure Portal)
- **CLI** (Befehlszeile, z.B. aws cli, az cli, gcloud, oc)
- **API / SDK** (per Programmcode, z.B. REST API, boto3 für Python)
