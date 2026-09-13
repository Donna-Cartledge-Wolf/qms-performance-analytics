# Data Dictionary

## Purpose

This document describes the synthetic datasets used in the Wolf Analytics QMS Performance & Change Management Analytics project.

All records are fictional and were generated for this portfolio project. No employer, client, patient, sponsor, confidential, proprietary, or personally identifiable data are included.

## `quality_events.csv`

Synthetic complaint and investigation records used to evaluate quality event aging, risk, overdue status, root cause patterns, and management priorities.

| Field | Type | Description |
|---|---|---|
| `event_id` | String | Unique identifier for each synthetic quality event. |
| `event_type` | String | Type of quality event. Values: `Investigation`, `Complaint`. |
| `process_area` | String | QMS process associated with the event. Values: `Risk Assessment`, `Supplier Quality`, `Change Management`, `CAPA`, `Document Control`, `Complaint Handling`, `Investigation / RCA`, `QMS Metrics`. |
| `opened_date` | Date stored as string | Date the synthetic quality event was opened. |
| `closed_date` | Date stored as string | Date the event was closed, when applicable. |
| `status` | String | Current event status. Values: `Open`, `Closed`. |
| `severity` | String | Assigned event severity. Values: `Low`, `Medium`, `High`, `Critical`. |
| `root_cause_category` | String | Root cause category assigned to the event. Values: `Process Design`, `Training`, `Equipment`, `Data / Documentation`, `Supplier`, `Procedure`, `Material`. |
| `target_days` | Integer | Scenario target duration for the event. Values: 15, 30, 45, or 60 days. |
| `age_days` | Integer | Calculated event age in days. Values in the generated dataset range from 3 to 90 days. |
| `overdue` | Boolean | Indicates whether the event is overdue according to the synthetic scenario logic. |
| `high_risk` | Boolean | Indicates whether the event is classified as high risk according to the synthetic scenario logic. |

## `capas.csv`

Synthetic CAPA records used to evaluate backlog, aging, risk, completion, overdue status, and effectiveness.

| Field | Type | Description |
|---|---|---|
| `capa_id` | String | Unique identifier for each synthetic CAPA. |
| `source` | String | Origin of the CAPA. Values: `Supplier`, `Investigation`, `Complaint`, `Audit`, `Trend`. |
| `opened_date` | Date stored as string | Date the CAPA was opened. |
| `due_date` | Date stored as string | Assigned due date for the CAPA. |
| `completion_date` | Date stored as string | Date the CAPA was completed, when applicable. |
| `status` | String | Current CAPA status. Values: `Open`, `Closed`. |
| `risk_level` | String | Assigned CAPA risk level. Values: `Low`, `Medium`, `High`. |
| `effectiveness_result` | String | CAPA effectiveness assessment result. Values: `Pending`, `Effective`, `Ineffective`. |
| `overdue` | Boolean | Indicates whether the CAPA is overdue according to the synthetic scenario logic. |
| `cycle_days` | Float | Calculated CAPA cycle duration in days. Values in the generated dataset range from 5 to 100 days. |

## `changes.csv`

Synthetic change control records used to evaluate implementation cycle time, risk, training completion, verification, follow-up needs, and closure readiness.

| Field | Type | Description |
|---|---|---|
| `change_id` | String | Unique identifier for each synthetic change record. |
| `change_type` | String | Type of change. Values: `Training`, `Document`, `Process`, `ERP / Software`, `Equipment`, `Supplier`. |
| `submitted_date` | Date stored as string | Date the change was submitted. |
| `implemented_date` | Date stored as string | Date the change was implemented, when applicable. |
| `status` | String | Current change status. Values: `In Progress`, `Implemented`, `Closed`. |
| `risk_level` | String | Assigned change risk level. Values: `Low`, `Medium`, `High`. |
| `approval_days` | Integer | Number of days associated with the approval step. Values range from 2 to 15 days. |
| `training_required` | Boolean | Indicates whether training is required for the change. |
| `training_complete_pct` | Integer | Percentage of required training completed. Values range from 0 to 100. |
| `verification_complete` | Boolean | Indicates whether change verification has been completed. |
| `follow_up_pending` | Boolean | Indicates whether additional follow-up remains after implementation. |
| `ready_for_closure` | Boolean | Indicates whether the change meets the synthetic scenario conditions for closure readiness. |
| `cycle_days` | Float | Calculated change cycle duration in days. Values in the generated dataset range from 5 to 322 days. |

## `training_coverage.csv`

Synthetic organizational capability data used to evaluate qualified staffing, backup coverage, capability gaps, and single-point-of-failure risk across QMS processes.

| Field | Type | Description |
|---|---|---|
| `process` | String | QMS process evaluated for capability coverage. Values: `Complaint Handling`, `Investigation / RCA`, `CAPA`, `Change Management`, `Supplier Quality`, `QMS Metrics`, `Document Control`, `Risk Assessment`. |
| `qualified_personnel` | Integer | Number of personnel considered qualified for the process in the synthetic scenario. |
| `required_coverage` | Integer | Number of qualified personnel specified as the required coverage for the process in the synthetic scenario. |
| `backup_personnel` | Integer | Number of personnel available as qualified backup coverage. |
| `coverage_pct` | Float | Calculated percentage of required process coverage. Values in the generated dataset are 80.0%, 83.3%, and 100.0%. |
| `single_point_failure` | Boolean | Indicates whether the process has a single point of failure because qualified backup coverage is not available. |

## Data Relationships

The four datasets represent different parts of the synthetic QMS scenario:

- `quality_events.csv` contains complaints and investigations.
- `capas.csv` contains CAPA records.
- `changes.csv` contains change control records.
- `training_coverage.csv` contains organizational capability and staffing coverage data.

The analytics workflow uses these datasets together to evaluate quality system performance, risk, backlog, CAPA effectiveness, change execution, root cause patterns, capability gaps, and management priorities.

## Data Quality

The synthetic datasets are subject to automated integrity checks and independent human plausibility review.

QC includes checks for:

- Date chronology
- Status and date consistency
- Overdue calculations
- CAPA lifecycle logic
- Change management lifecycle logic
- Training and capability coverage
- Single-point-of-failure logic
- Operational plausibility

See `QC_METHODS.md` for additional details.

## Scope

The field definitions and values in this document describe this synthetic portfolio scenario only.

They are not presented as industry standards, regulatory requirements, medical device QMS specifications, or acceptance criteria.
