# PrivacyGuard — Social Media Privacy Risk Assessment Framework

## Overview

**PrivacyGuard** is a defensive, privacy-first cybersecurity project that helps users understand potential privacy and security risks associated with their social-media habits and settings.

The system uses a questionnaire-based assessment to calculate a **Privacy Risk Score from 0–100**, classify the assessed risk level, identify major privacy weaknesses, and provide practical recommendations for improving privacy and security.

The project is designed for **educational, defensive, and privacy-awareness purposes**.

---

## Objectives

The main objectives of PrivacyGuard are to:

* Assess common social-media privacy risks.
* Calculate category-wise privacy risk scores.
* Generate an overall Privacy Risk Score.
* Classify the assessment into four risk levels.
* Identify important privacy weaknesses.
* Provide personalized privacy recommendations.
* Demonstrate how privacy-by-design principles can be implemented.
* Provide synthetic data for dashboard and testing purposes.
* Demonstrate defensive cybersecurity concepts without accessing real social-media accounts.

---

## Key Features

### 🔐 Privacy Assessment

The application contains **42 privacy and security questions** covering common social-media risks.

### 📊 Risk Scoring

The system calculates:

* Overall Privacy Risk Score
* Category-level scores
* Risk classification
* Findings
* Recommendations

### 🚦 Risk Classification

|  Score | Risk Level |
| -----: | ---------- |
|   0–20 | LOW        |
|  21–40 | MODERATE   |
|  41–70 | HIGH       |
| 71–100 | CRITICAL   |

A higher score represents greater assessed privacy exposure.

### 📋 Privacy Checklist

Users receive a practical checklist covering privacy and account-security improvements.

### 🔄 Improvement Simulator

The application provides a simulation showing how the score could change when higher-risk responses are replaced with lower-risk choices.

The simulator is educational and does **not guarantee future security or privacy**.

### 📈 Dashboard

The dashboard provides aggregate statistics and visual analysis of synthetic assessment data.

### 🧪 Synthetic Dataset

The project includes **1,000 fictional privacy-assessment records** for testing and demonstration.

### 🛡️ Defensive Design

The application does not:

* Scrape social-media profiles
* Track individuals
* Enumerate accounts
* Collect passwords
* Collect private messages
* Collect exact locations
* Bypass privacy controls
* Collect real social-media credentials

---

## Risk Categories

PrivacyGuard evaluates ten categories:

| Category             | Weight |
| -------------------- | -----: |
| Profile Visibility   |    10% |
| Personal Information |    15% |
| Location Privacy     |    15% |
| Posts & Content      |    10% |
| Connections          |    10% |
| Tagging & Mentions   |     5% |
| Account Security     |    15% |
| Third-Party Apps     |     5% |
| Social Engineering   |    10% |
| Digital Footprint    |     5% |

The overall score is calculated using the weighted category scores.

---

## System Workflow

```text
User
  ↓
Privacy Questionnaire
  ↓
Input Validation
  ↓
Feature Extraction
  ↓
Category Risk Analysis
  ↓
Risk Scoring Engine
  ↓
Overall Risk Score
  ↓
Risk Classification
  ↓
Findings
  ↓
Recommendations
  ↓
Dashboard / Report
```

---

## Technology Stack

### Backend

* Python
* Flask
* Flask-CORS
* SQLite

### Frontend

* HTML5
* CSS3
* JavaScript
* Chart.js

### Testing

* pytest

### Reporting

* ReportLab

### Deployment

* Gunicorn
* Render

---

## Project Structure

```text
Social-Media-Privacy-Risk-Assessment/
│
├── backend/
│   ├── __init__.py
│   ├── app.py
│   ├── database.py
│   └── services/
│       ├── __init__.py
│       ├── questions.py
│       └── risk_engine.py
│
├── frontend/
│   ├── index.html
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
│
├── data/
│   ├── generate_data.py
│   └── social_media_privacy_assessments.csv
│
├── docs/
│   ├── THREAT_MODEL.md
│   └── report/
│       └── PROJECT_REPORT.md
│
├── tests/
│   └── test_app.py
│
├── requirements.txt
└── .gitignore
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/vyshnaviporandla/Social-Media-Privacy-Risk-Assessment.git
```

Enter the project directory:

```bash
cd Social-Media-Privacy-Risk-Assessment
```

Create a virtual environment:

```cmd
python -m venv venv
```

Activate it:

```cmd
venv\Scripts\activate
```

Install dependencies:

```cmd
pip install -r requirements.txt
```

---

## Generate Synthetic Data

Run:

```cmd
python data\generate_data.py
```

The generated dataset is stored at:

```text
data/social_media_privacy_assessments.csv
```

The dataset contains fictional records and is intended for testing and demonstration.

---

## Run the Application

Start the Flask server:

```cmd
python backend\app.py
```

Open the application in a browser:

```text
http://127.0.0.1:5000
```

---

## Run Tests

Run the automated tests with:

```cmd
python -m pytest
```

---

## REST API

| Method | Endpoint                               | Description                   |
| ------ | -------------------------------------- | ----------------------------- |
| GET    | `/api/questions`                       | Retrieve assessment questions |
| POST   | `/api/assessment`                      | Create a privacy assessment   |
| GET    | `/api/assessment/<id>`                 | Retrieve an assessment        |
| GET    | `/api/assessment/<id>/recommendations` | Retrieve recommendations      |
| POST   | `/api/assessment/simulate-improvement` | Simulate improvements         |
| GET    | `/api/dashboard/stats`                 | Retrieve dashboard statistics |
| GET    | `/api/privacy-checklist`               | Retrieve privacy checklist    |

---

## Privacy-by-Design

PrivacyGuard follows a privacy-first approach.

The questionnaire focuses on whether information or settings are exposed rather than asking users to provide the actual sensitive information.

The application does not require:

* Phone numbers
* Email addresses
* Home addresses
* Birth dates
* Passwords
* Private messages
* Exact geographic coordinates
* Social-media credentials

---

## Threat Model

The project includes a dedicated threat model covering:

* Assets
* Threats
* Security controls
* Trust boundaries
* Privacy risks
* Residual risks
* Excluded misuse cases

See:

```text
docs/THREAT_MODEL.md
```

---

## Limitations

PrivacyGuard is an educational risk-assessment framework.

Its limitations include:

* Results depend on questionnaire answers.
* It does not inspect actual social-media account settings.
* Different platforms provide different privacy controls.
* The score is an indicator of assessed exposure, not a guarantee of security.
* Synthetic data is used for demonstration.
* The improvement simulator represents a hypothetical scenario.

---

## Future Enhancements

Possible future improvements include:

* Platform-specific privacy checklists
* More assessment questions
* Expanded reporting
* Additional dashboard analytics
* Optional local photo metadata awareness
* More automated tests
* Privacy-preserving historical score tracking
* Additional educational modules

---

## Ethical Scope

PrivacyGuard is intended for **defensive cybersecurity and privacy awareness**.

It should only be used with information that the user is authorized to assess.

The project intentionally excludes social-media scraping, account enumeration, credential collection, tracking, privacy-control bypassing, and private-message monitoring.

---

## Author

**Vyshnavi Porandla**

Academic defensive cybersecurity project.

## GitHub

https://github.com/vyshnaviporandla/Social-Media-Privacy-Risk-Assessment
