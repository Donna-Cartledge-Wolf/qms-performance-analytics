# Project Plan

This project is being developed in stages, with each phase building on a validated synthetic QMS dataset.

## Phase 1: Foundation

**Status: Complete**

- Generate synthetic complaints, investigations, CAPAs, change records, and training coverage data
- Build reproducible data generation using a fixed random seed
- Perform automated integrity checks
- Perform independent human plausibility review
- Document the QC approach in `QC_METHODS.md`
- Finalize a realistic but intentionally imperfect QMS scenario

## Phase 2: Analysis

**Status: Core analysis complete**

Calculate and review:

- Quality event aging and overdue rate
- High-risk open quality events
- CAPA aging and overdue rate
- CAPA effectiveness
- Change implementation cycle time
- Change follow-up backlog
- Training and cross-training coverage
- Single-point-of-failure exposure
- Root-cause recurrence and trend analysis

The KPI engine compares selected measures with portfolio scenario targets and identifies areas that require management attention.

Scenario targets are used for demonstration purposes and are not presented as industry benchmarks.

## Phase 3: Management Review Dashboard

**Status: In progress**

Build an interactive dashboard that presents:

- Executive KPI cards
- PASS and ACTION status indicators
- Quality event aging and risk
- CAPA backlog and effectiveness
- Change management performance
- Root-cause and recurrence trends
- Training and capability gaps
- High-risk items requiring attention
- Management priorities and decision support

The dashboard will use the validated synthetic dataset and the independently checked KPI calculations.

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
