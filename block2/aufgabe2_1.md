# Auftrag 2.1: Dienstleistungen von Cloud-Anbietern vergleichen

Erstellen Sie eine vergleichende Analyse der Dienstleistungen führender Cloud-Anbieter.

## Anbieterauswahl: Wählen Sie mindestens drei führende Anbieter aus (z. B. AWS, Azure, Google Cloud).

- **AWS (Amazon Web Services):** Marktführer, ca. 30% Marktanteil, seit 2006
- **Microsoft Azure:** Nr. 2, ca. 20-22%, stark bei Firmen mit Microsoft Produkten
- **Google Cloud Platform (GCP):** Nr. 3, ca. 12-13%, stark bei Daten, AI und Kubernetes
- Alle drei haben eine Region in Zürich (wichtig für Daten in der Schweiz)

## Portfolio: Stellen Sie die wichtigsten Dienstleistungen vor (z. B. Speicher, Datenbanken, AI/ML, Netzwerk).

| Bereich | AWS | Azure | Google Cloud |
|---|---|---|---|
| Compute (VMs) | EC2 | Virtual Machines | Compute Engine |
| Serverless | Lambda | Azure Functions | Cloud Run Functions |
| Container / K8s | ECS, EKS | AKS, Container Apps | GKE, Cloud Run |
| Object Storage | S3 | Blob Storage | Cloud Storage |
| Datenbank SQL | RDS, Aurora | Azure SQL Database | Cloud SQL, AlloyDB, Spanner |
| Datenbank NoSQL | DynamoDB | Cosmos DB | Firestore, Bigtable |
| Data Warehouse | Redshift | Synapse, Fabric | BigQuery |
| AI / ML | SageMaker, Bedrock | Azure ML, Azure OpenAI | Vertex AI, Gemini |
| Netzwerk | VPC, Route 53, CloudFront | VNet, Azure DNS, Front Door | VPC, Cloud DNS, Cloud CDN |
| Identität | IAM | Entra ID (ex Azure AD) | Cloud IAM |
| Monitoring | CloudWatch, CloudTrail | Azure Monitor | Cloud Monitoring, Cloud Logging |
| IaC | CloudFormation | ARM / Bicep | Infrastructure Manager (Terraform) |

## Vergleichsmatrix: Analysieren Sie die Anbieter anhand der Kriterien: Kostenstruktur, Skalierbarkeit, Sicherheit, Verfügbarkeit und Support.

| Kriterium | AWS | Azure | Google Cloud |
|---|---|---|---|
| Fokus | Umfangreichstes Portfolio | Enterprise und Hybrid | Daten, AI und Analytics |
| Stärken | Marktführer, sehr ausgereift, grösste Community | Microsoft Ökosystem (M365, AD, Windows Server), Hybrid mit Azure Arc | Kubernetes (von Google erfunden), BigQuery, schnelles Netzwerk |
| Kostenstruktur | Pay-per-Use, Abrechnung pro Sekunde, Reserved Instances, Savings Plans, Spot, Free Tier | Pay-per-Use, Reserved Instances, Hybrid Benefit (eigene Windows/SQL Lizenzen weiterverwenden), Spot, 200 USD Startguthaben | Pay-per-Use, automatische Rabatte bei Dauerbetrieb (Sustained Use), Committed Use, Spot VMs, 300 USD Startguthaben |
| Skalierbarkeit | Auto Scaling Groups, sehr viele Instanztypen | VM Scale Sets, App Service Autoscale | Managed Instance Groups, GKE Autopilot, sehr schnelles Scaling |
| Sicherheit | IAM sehr fein einstellbar, KMS, GuardDuty, Security Hub | Entra ID, Defender for Cloud, Key Vault, Sentinel | Cloud IAM, Security Command Center, Verschlüsselung standardmässig |
| Zertifizierungen | ISO 27001, SOC 2, DSG/DSGVO | ISO 27001, SOC 2, DSG/DSGVO | ISO 27001, SOC 2, DSG/DSGVO |
| Verfügbarkeit | meiste Availability Zones, ca. 35+ Regionen, Zürich, SLA bis 99.99% | meiste Regionen (60+), Zürich und Genf, SLA bis 99.99% | ca. 40 Regionen, Zürich (europe-west6), SLA bis 99.99% |
| Support | Basic (gratis), Developer, Business, Enterprise, sehr grosse Doku und Community | Basic (gratis), Developer, Standard, Professional Direct, Unified, gut integriert mit MS Partnern | Basic (gratis), Standard, Enhanced, Premium, gute Doku, kleinere Community |

## Fazit

- **AWS:** wenn man das grösste Angebot und am meisten Erfahrung will
- **Azure:** wenn die Firma schon mit Microsoft arbeitet (M365, Active Directory, Windows)
- **Google Cloud:** wenn Daten, AI oder Kubernetes im Mittelpunkt stehen
- Kosten hängen stark vom Anwendungsfall ab, darum mit dem Pricing Calculator vergleichen: AWS Pricing Calculator, Azure Pricing Calculator, Google Cloud Pricing Calculator
