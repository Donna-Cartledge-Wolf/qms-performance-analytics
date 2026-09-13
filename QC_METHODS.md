# QC Methods

## Purpose

Wolf Analytics uses two complementary QC steps for this portfolio project:

1. Automated technical QC
2. Independent human plausibility review

A successful code run is not, by itself, evidence that a dataset or result is scientifically or operationally credible. The QC process is intended to verify both technical consistency and real-world plausibility before results are interpreted or presented.

## Automated Technical QC

Automated checks include:

- No future opening, completion, closure, or implementation dates
- No completion or closure date before the corresponding originating date
- Status and date consistency
- Verification of overdue calculations
- CAPA effectiveness-state consistency
- Change management lifecycle consistency
- Training coverage calculation checks
- Single-point-of-failure flag checks
- Reproducible synthetic data generation using a fixed random seed

These checks are intended to identify structural errors, impossible timelines, inconsistent status logic, and calculation problems before the data are used for KPI analysis or visualization.

## Human Plausibility Review

Human QC evaluates whether the generated records and resulting metrics make sense in a realistic quality management setting.

Questions considered during review include:

- Is event aging believable?
- Is the overdue backlog plausible rather than randomly extreme?
- Do severity, risk, status, and due-date relationships make operational sense?
- Does the CAPA effectiveness calculation use an appropriate denominator?
- Are change implementation, training, verification, and closure represented as distinct lifecycle states?
- Do staffing and cross-training levels resemble a functioning organization?
- Can a manager identify what requires attention and understand why?
- Are conclusions supported by the underlying data rather than by the appearance of the visualization?

Human review is performed independently of whether the code executes successfully.

## Scenario Design

The synthetic organization is intentionally modeled as generally well controlled, but not perfect.

The scenario includes:

- Most QMS processes operating within expected controls
- A manageable subset of overdue or high-risk quality events
- Strong, but not perfect, CAPA effectiveness
- A realistic change management follow-up backlog
- Generally strong organizational capability and cross-training coverage
- One intentional single-point-of-failure dependency that remains visible for management attention

These values are design choices for this portfolio project. They are not presented as industry benchmarks or regulatory acceptance criteria.

## Use of Results

Numerical results are not used in resume, LinkedIn, or portfolio claims until they are:

- Reproducibly generated
- Technically validated
- Independently reviewed for plausibility
- Traceable to the underlying synthetic dataset

This rule is intended to keep portfolio claims consistent with the evidence produced by the project.

## Data Privacy

All project data are synthetic.

No employer, client, patient, sponsor, proprietary, confidential, or personally identifiable records are used.
