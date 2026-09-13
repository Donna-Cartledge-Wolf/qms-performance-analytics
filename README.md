<p align="center">
  <img src="assets/Wolf_Analytics_Logo.png" alt="Wolf Analytics logo" width="240">
</p>

# Wolf Analytics: QMS Performance & Change Management Analytics

Python-based portfolio project using 100% synthetic data to demonstrate quality systems analytics, performance monitoring, risk prioritization, and management review decision support.

## Project Overview

The project models a realistic but intentionally imperfect QMS environment and converts synthetic quality records into management-level performance measures.

The workflow includes:

- Synthetic QMS data generation
- Automated data integrity checks
- Independent human plausibility review
- KPI calculation and management review logic
- Root cause frequency and trend analysis
- CAPA performance analysis
- Change management performance analysis
- Training and organizational capability assessment
- Interactive Streamlit dashboard

## Management Review Report

A formatted management review report generated from the interactive dashboard is available here:

[View the QMS Management Review Report](outputs/Wolf_Analytics_QMS_Management_Review.pdf)

## Management Review Focus

The analysis evaluates:

- Quality event aging and overdue status
- High-risk open quality events
- CAPA backlog and effectiveness
- Change implementation cycle time
- Change follow-up needs
- Root cause frequency, risk, and monthly trends
- Training and cross-training coverage
- Single-point-of-failure exposure
- Management priorities and decision support

## Verified Project Results

The validated synthetic QMS scenario contains:

- 180 quality events
- 40 open quality events
- 8 overdue open quality events
- 11 high-risk open quality events
- 95 CAPAs
- 18 open CAPAs
- 2 overdue open CAPAs
- 91.0% CAPA effectiveness
- 72 closed changes
- 21 changes awaiting follow-up
- 27 changes in progress
- 6 high-risk changes not closed
- 26-day median change implementation cycle
- 90.8% mean organizational capability coverage
- 1 identified single-point-of-failure dependency

The management review logic classified:

- 4 KPI areas as requiring management action
- 2 KPI areas as meeting the portfolio target

Scenario targets are used for portfolio demonstration only and are not presented as industry benchmarks or regulatory acceptance criteria.

## Management Review Dashboard

The Streamlit dashboard brings the validated data and KPI calculations together in a single management review view.

Dashboard sections include:

- Management Priorities
- Executive KPI Overview
- Quality Event Aging and Risk
- Root-Cause Frequency and Risk
- Root-Cause Trend by Month
- CAPA Performance
- Change Management Performance
- Training and Organizational Capability
- Single-Point-of-Failure Exposure
- Management Review Status

## Quality Control

The project uses two complementary QC steps:

1. Automated technical QC
2. Independent human plausibility review

Automated checks evaluate date chronology, status and date consistency, overdue calculations, CAPA lifecycle logic, change management lifecycle logic, training coverage calculations, and single-point-of-failure logic.

The KPI results were also independently recalculated and reconciled with the primary analytics engine.

Human review evaluates whether the synthetic records, KPI values, risk patterns, and management conclusions are operationally believable.

See `QC_METHODS.md` for the full QC approach.

## Quick Start

```bash
pip install -r requirements.txt
python src/generate_synthetic_qms_data.py
python src/qms_metrics.py
streamlit run src/qms_dashboard.py
```

## Repository Structure

```text
qms-performance-analytics/
├── assets/
├── config/
├── data/
├── outputs/
├── src/
│   ├── generate_synthetic_qms_data.py
│   ├── qms_metrics.py
│   └── qms_dashboard.py
├── PROJECT_PLAN.md
├── QC_METHODS.md
├── RESUME_EVIDENCE.md
├── README.md
└── requirements.txt
```

## Data and Scope

All data in this repository are synthetic.

The project contains no employer, client, patient, sponsor, confidential, proprietary, or personally identifiable data.

It demonstrates analytical, quality systems, and management review thinking. It does not claim ownership or operation of a commercial medical device QMS, ISO certification, or direct commercial medical device manufacturing experience.

## Purpose

The goal is to demonstrate how Python-based analytics can turn quality system records into clear performance measures that help identify aging issues, CAPA risk, change management follow-up needs, root cause patterns, organizational capability gaps, and management priorities.
