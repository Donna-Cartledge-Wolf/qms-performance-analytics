# QC Methods

## Purpose

Wolf Analytics uses two complementary QC steps for this portfolio project:

1. Automated technical QC
2. Independent human plausibility review

A successful code run is not, by itself, evidence that a dataset or result is technically sound or operationally believable. The QC process checks both data integrity and plausibility before results are interpreted or presented.

## Automated Technical QC

Automated checks include:

- No future opening, completion, closure, or implementation dates
- No completion or closure date before the corresponding originating date
- Status and date consistency
- Overdue calculation checks
- CAPA effectiveness-state consistency
- Change management lifecycle consistency
- Training and capability coverage calculations
- Single-point-of-failure logic
- Reproducible synthetic data generation using a fixed random seed

These checks identify structural errors, impossible timelines, inconsistent status logic, and calculation problems before the data are used for KPI analysis or visualization.

## Human Plausibility Review

Human QC evaluates whether the generated records, calculated metrics, and management conclusions make sense in a realistic quality management setting.

Questions considered during review include:

- Is quality event aging believable?
- Is the overdue backlog plausible rather than randomly extreme?
- Do severity, risk, status, and due date relationships make operational sense?
- Does the CAPA effectiveness calculation use an appropriate denominator?
- Are change implementation, training, verification, follow-up, and closure represented as distinct lifecycle states?
- Do root cause frequencies and trends appear plausible within the synthetic scenario?
- Do staffing, capability, and cross-training levels resemble a functioning organization?
- Can a manager identify what requires attention and understand why?
- Are management conclusions supported by the underlying data rather than by the appearance of a visualization?

Human review is performed independently of whether the code executes successfully.

## KPI Reconciliation

Key KPI results were independently recalculated and compared with the primary analytics engine.

The reconciliation included measures such as:

- Open and overdue quality events
- High-risk open quality events
- Open and overdue CAPAs
- CAPA effectiveness
- Change management cycle time
- Change follow-up backlog
- High-risk changes not closed
- Organizational capability coverage
- Single-point-of-failure exposure

The independently calculated values matched the primary KPI outputs.

## Scenario Design

The synthetic organization is intentionally modeled as generally well controlled, but not perfect.

The scenario includes:

- Most QMS processes operating within the intended portfolio controls
- A manageable subset of overdue or high-risk quality events
- Strong, but not perfect, CAPA effectiveness
- A realistic change management follow-up backlog
- Generally strong organizational capability and cross-training coverage
- One intentional single point of failure that remains visible for management attention

These values are design choices for this portfolio project. They are not presented as industry benchmarks, regulatory requirements, or acceptance criteria.

## Dashboard and Presentation Review

The final management review dashboard was reviewed for:

- Consistency with the validated KPI outputs
- Accurate representation of root cause patterns and trends
- Correct identification of high-risk and overdue items
- Consistency between management priorities and the underlying calculations
- Clear distinction between portfolio targets and industry benchmarks
- Readability and presentation consistency

Presentation changes were not allowed to alter the validated analytical logic.

## Use of Results

Numerical results are not used in resume, LinkedIn, GitHub, or portfolio claims until they are:

- Reproducibly generated
- Technically validated
- Independently reviewed for plausibility
- Traceable to the underlying synthetic dataset

This rule keeps professional claims consistent with the evidence produced by the project.

## Data Privacy

All project data are synthetic.

No employer, client, patient, sponsor, proprietary, confidential, or personally identifiable records are used.
