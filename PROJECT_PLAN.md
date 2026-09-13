# Project Plan

This project was developed in stages, with each phase building on a validated synthetic QMS dataset.

## Phase 1: Foundation

**Status: Complete**

- Generated synthetic complaints, investigations, CAPAs, change records, and training coverage data
- Built reproducible data generation using a fixed random seed
- Performed automated integrity checks
- Performed an independent human plausibility review
- Documented the QC approach in `QC_METHODS.md`
- Finalized a realistic but intentionally imperfect QMS scenario

## Phase 2: Analysis

**Status: Complete**

Calculated and reviewed:

- Quality event aging and overdue rate
- High-risk open quality events
- CAPA aging and overdue rate
- CAPA effectiveness
- Change implementation cycle time
- Change follow-up backlog
- Training and cross-training coverage
- Single-point-of-failure exposure
- Root cause frequency, risk, and monthly trends

The KPI engine compares selected measures with portfolio scenario targets and identifies areas that require management attention.

Scenario targets are used for demonstration purposes and are not presented as industry benchmarks.

## Phase 3: Management Review Dashboard

**Status: Complete**

Built an interactive management review dashboard that presents:

- Executive KPI cards
- PASS and ACTION status indicators
- Quality event aging and risk
- CAPA backlog and effectiveness
- Change management performance
- Root cause frequency, risk, and monthly trends
- Training and organizational capability gaps
- High-risk items requiring management attention
- Single-point-of-failure exposure
- Management priorities and decision support

The dashboard uses the validated synthetic QMS dataset and independently checked KPI calculations. It brings quality event, CAPA, change management, root cause, and organizational capability metrics together in a management review view.

## Phase 4: Portfolio Completion

**Status: In progress**

Complete the project documentation and presentation by adding:

- Dashboard screenshots
- Data dictionary
- Final methodology notes
- QC documentation
- Repository branding
- Resume-ready quantified project evidence
- Final human review of technical claims and presentation

Only results that are reproducible, validated, and traceable to the synthetic source data will be used in professional portfolio or resume claims.
