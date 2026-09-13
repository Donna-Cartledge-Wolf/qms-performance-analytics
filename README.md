<p align="center">
  <img src="assets/Wolf_Analytics_Logo.png" alt="Wolf Analytics logo" width="240">
</p>

# Wolf Analytics: QMS Performance & Change Management Analytics

Portfolio project using 100% synthetic data to demonstrate quality systems analytics, performance monitoring, and management review decision support.

## Focus

- Complaint and investigation aging
- CAPA status, backlog, and effectiveness
- Change management cycle time and follow-up
- Risk prioritization
- Process performance indicators
- Training and cross-training coverage
- Single-point-of-failure risk
- Management review decision support

## Quick Start

```bash
pip install -r requirements.txt
python src/generate_synthetic_qms_data.py
python src/qms_metrics.py
streamlit run src/qms_dashboard.py
```

## Quality Control

The project uses both automated technical checks and independent human plausibility review.

QC includes checks for date and status consistency, overdue calculations, CAPA effectiveness logic, change management lifecycle integrity, training coverage calculations, and overall operational plausibility.

See `QC_METHODS.md` for the full QC approach.

## Data and Scope

All data in this repository are synthetic.

The project contains no employer, client, patient, sponsor, confidential, or proprietary data. It demonstrates analytical, quality systems, and management review thinking.

It does not claim ownership or operation of a commercial medical device QMS, ISO certification, or direct commercial medical device manufacturing experience.

## Purpose

The goal is to demonstrate how Python-based analytics can turn quality system records into clear performance measures that help identify aging issues, CAPA risk, change management follow-up needs, capability gaps, and management priorities.
