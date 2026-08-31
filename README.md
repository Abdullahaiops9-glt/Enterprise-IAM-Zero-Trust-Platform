# IAM Zero Trust Platform

Enterprise Identity & Access Management with Zero Trust, Behavioral Analytics, and Automated Governance.

## Overview

This project implements a complete IAM Zero Trust architecture for the EduQual Level 6 Diploma.
Every component is deployed and executable — not just diagrams. The platform includes Docker-based Keycloak deployment,
a full ML risk pipeline, automated governance, PAM with break-glass, threat simulation, and compliance reporting.

## What This Project Does

- Deploys Keycloak as Identity Provider using Docker
- Generates synthetic user behavior data (5000 records)
- Engineers risk features from login patterns
- Trains Isolation Forest (unsupervised) + Random Forest (supervised)
- Produces 0-100 risk scores via ensemble model
- Makes policy decisions: ALLOW / STEP_UP_MFA / DENY
- Automates identity lifecycle and segregation of duties
- Manages privileged access with JIT and break-glass
- Simulates threat response for 3 attack scenarios
- Generates compliance dashboard with charts

## Architecture
User Request → Keycloak IdP → Risk Engine (ML) → Policy Decision Point → Policy Enforcement → Enterprise Resources
      ↓              ↓                    ↓
SAML/mTLS      Behavioral Analytics   Governance & Audit

---

## Tools Used

Python, Pandas, NumPy, Scikit-learn, Matplotlib, Docker, Keycloak, HashiCorp Vault

## Project Structure

iam-zero-trust-platform/

├── docker-compose.yml              # Keycloak Docker deployment

├── requirements.txt               # Python dependencies

├── README.md                      # This file

├── keycloak/

│   ├── setup_realm.py             # Realm, users, roles config

│   └── enterprise-iam-realm.json  # Generated realm file

├── saml/

│   ├── federation.py              # SAML metadata exchange

│   ├── idp1_metadata.xml          # Generated

│   └── idp2_metadata.xml          # Generated

├── certs/

│   ├── generate_certs.py          # mTLS certificate generation

│   ├── gateway_cert.pem           # Generated

│   └── keycloak_cert.pem          # Generated

├── ml_pipeline/

│   ├── 01_generate_data.py        # 5000 synthetic records

│   ├── 02_feature_engineering.py  # 7 risk features

│   ├── 03_baseline_modeling.py    # Per-user behavior baseline

│   ├── 04_isolation_forest.py     # Unsupervised anomaly detection

│   ├── 05_random_forest.py        # Supervised classification

│   ├── 06_risk_scoring.py         # 0-100 ensemble score

│   └── 07_pdp_integration.py      # ALLOW / MFA / DENY decisions

├── governance/

│   ├── 08_lifecycle_sod.py        # Joiner/Mover/Leaver + SoD

│   └── 09_access_recertification.py # Automated access reviews

├── pam/

│   └── 10_pam_jit_breakglass.py   # JIT + emergency access

├── threat_response/

│   └── 11_threat_simulation.py    # 3 attack scenarios

├── reporting/

│   └── 12_compliance_dashboard.py # Audit dashboard + charts

├── demo/

│   └── 13_end_to_end_orchestration.py # Full IAM flow demo

├── docs/

│   └── pam_comparison.py          # Vault vs CyberArk analysis

└── outputs/

├── df.csv                     # Generated dataset

├── rf_model.pkl               # Saved ML model

├── isolation_forest.png       # Anomaly distribution chart

├── risk_distribution.png      # Risk score histogram

├── decision_pie.png           # Access decision breakdown

├── feature_importance.png     # ML feature ranking

└── detection_accuracy.png     # True/False positive chart

---

## Prerequisites

- Ubuntu 22.04+ (or any Linux VM)
- Docker & Docker Compose
- Python 3.11+
- pip3
- git

---

## Installation

```bash
### 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/iam-zero-trust-platform.git
cd iam-zero-trust-platform

### 2. Install Docker & Python libraries
Install Docker, Python 3, pip, git
pip3 install -r requirements.txt --break-system-packages

### 3. Create output directory
mkdir -p outputs

## How to Run

Execute scripts in this exact order:

# Deploy Identity Provider
docker-compose up -d

# Configure Keycloak realm
python3 keycloak/setup_realm.py

# SAML federation
python3 saml/federation.py

# mTLS certificates
python3 certs/generate_certs.py

# ML Pipeline
- python3 ml_pipeline/01_generate_data.py
- python3 ml_pipeline/02_feature_engineering.py
- python3 ml_pipeline/03_baseline_modeling.py
- python3 ml_pipeline/04_isolation_forest.py
- python3 ml_pipeline/05_random_forest.py
- python3 ml_pipeline/06_risk_scoring.py
- python3 ml_pipeline/07_pdp_integration.py

# Governance
- python3 governance/08_lifecycle_sod.py
- python3 governance/09_access_recertification.py

# Privileged Access
- python3 pam/10_pam_jit_breakglass.py

# Threat Response
- python3 threat_response/11_threat_simulation.py

# Compliance Dashboard
- python3 reporting/12_compliance_dashboard.py

# End-to-End Demo
- python3 demo/13_end_to_end_orchestration.py

## What Each Component Does

| Script | Purpose | Output |
|---|---|---|
| `setup_realm.py` | Configures Keycloak realm with roles, users, and brute-force protection | `enterprise-iam-realm.json` |
| `federation.py` | SAML metadata exchange between two IdPs | `idp1_metadata.xml`, `idp2_metadata.xml` |
| `generate_certs.py` | Generates X.509 certificates and performs mTLS handshake | `gateway_cert.pem`, `keycloak_cert.pem` |
| `01_generate_data.py` | Generates 5,000 synthetic sessions with 250 anomalies | `outputs/df.csv` |
| `02_feature_engineering.py` | Creates 7 risk features and behavior score | Updated `df.csv` |
| `03_baseline_modeling.py` | Establishes per-user normal behavior baseline | Updated `df.csv` |
| `04_isolation_forest.py` | Performs unsupervised anomaly detection | `isolation_forest.png` |
| `05_random_forest.py` | Performs supervised classification | `rf_model.pkl` |
| `06_risk_scoring.py` | Calculates weighted ensemble risk score from 0–100 | Updated `df.csv` |
| `07_pdp_integration.py` | Makes Zero Trust policy decisions | Terminal decision table |
| `08_lifecycle_sod.py` | Handles identity lifecycle and segregation of duties | Terminal governance table |
| `09_access_recertification.py` | Flags stale access and performs recertification checks | Terminal summary |
| `10_pam_jit_breakglass.py` | Implements JIT access and emergency break-glass access | Terminal audit trail |
| `11_threat_simulation.py` | Simulates 3 attack scenarios with automated response | Terminal threat logs |
| `12_compliance_dashboard.py` | Generates audit-ready compliance charts and metrics | 4 PNG charts |
| `13_end_to_end_orchestration.py` | Demonstrates the complete LOW/MEDIUM/HIGH risk flow | Terminal orchestration log |

## Screenshots & Evidence

The following 21 screenshots were captured during live execution:

- docker ps — Keycloak container running
- Browser — localhost:8080 Keycloak admin login
- Terminal — Realm JSON created with users and roles
- Terminal — SAML assertion_valid: True
- Terminal — mTLS mutual_auth: SUCCESS
- Terminal — 5000 records, 250 anomalies generated
- Terminal — Behavior score range output
- Terminal — Baseline created for 5000 users
- Terminal — Isolation Forest: 250 detected, 182 true caught
- Image — isolation_forest.png anomaly distribution
- Terminal — Random Forest Classification Report
- Terminal — Risk scoring: LOW 4204, MEDIUM 547, HIGH 249
- Terminal — PDP: ALLOW / STEP_UP_MFA / DENY table
- Terminal — Governance lifecycle + SoD rules
- Terminal — Access recertification summary
- Terminal — Break-glass emergency access audit
- Terminal — 3 threat scenarios with ACCESS_DENIED
- Terminal — Compliance metrics report
- Image — risk_distribution.png histogram
- Image — feature_importance.png ranking chart
- Terminal — End-to-end LOW/MEDIUM/HIGH demo

## Compliance Mapping

| Component | NIST 800-63 | ISO 27001 | GDPR | SOX |
|---|---|---|---|---|
| Keycloak IdP | Identity Assurance | Access Control | Data Protection | User Authentication |
| ML Risk Engine | Risk Adaptive | Monitoring | Breach Detection | Fraud Detection |
| Governance | Audit Logging | SoD / Reviews | Consent / Accuracy | Access Reviews |
| PAM / Break-Glass | Emergency Access | Privilege Control | Incident Response | Emergency Audit |
| Compliance Dashboard | Reporting | Audit Trail | Accountability | Financial Controls |

## Tools Used
- Python — Pandas, NumPy, Scikit-learn, Matplotlib, Cryptography
- Docker — Keycloak container deployment
- Keycloak — Identity Provider (SAML/OIDC/OAuth)
- HashiCorp Vault — PAM & secrets management (referenced)

## Author
### Abdullah
### EduQual Level 6 Diploma — Advanced IAM Orchestration
All architecture decisions, trade-off analysis, tool selection, and technical justifications are original and defensible in Q&A.

## License
Open-source implementation for academic demonstration. Enterprise alternatives (Okta, CyberArk) evaluated and documented in docs/pam_comparison.py.
