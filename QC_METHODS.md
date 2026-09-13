# QC Methods

## Purpose
Wolf Analytics uses a two-layer QC approach for this portfolio project:

1. **Automated technical QC**
2. **Independent human plausibility review**

The purpose is to prevent a successful code run from being mistaken for a scientifically or operationally credible result.

## Automated technical QC

Automated checks include:

- no future opening, completion, closure, or implementation dates
- no completion/closure date before the originating date
- status/date consistency
- overdue-flag calculation checks
- CAPA effectiveness-state consistency
- change-lifecycle consistency
- training-coverage calculation checks
- single-point-of-failure flag checks
- reproducible synthetic generation through a fixed random seed

## Human plausibility review

Human QC asks whether the generated records and metrics make sense in a realistic quality-management context.

Examples include:

- Is event aging believable?
- Is the overdue backlog plausible rather than randomly extreme?
- Do severity, risk, status, and due-date relationships make operational sense?
- Does CAPA effectiveness use an appropriate denominator?
- Are change implementation, training, verification, and closure modeled as distinct lifecycle states?
- Do staffing and cross-training levels resemble a functioning organization?
- Would a manager be able to identify what needs attention and why?
- Are conclusions supported by the underlying data rather than inferred from attractive visualizations?

## Scenario-design principle

The synthetic organization is intentionally designed as **healthy but imperfect**:

- most QMS processes are controlled
- a manageable subset of quality events is overdue or high risk
- CAPA effectiveness is strong but not perfect
- change management includes a realistic follow-up backlog
- organizational capability is generally strong
- one intentional single-point-of-failure dependency remains visible for management action

These values are portfolio scenario-design choices and are **not presented as industry benchmarks**.

## Resume / portfolio evidence rule

No numerical result is used in a resume, LinkedIn profile, or portfolio claim until it is:

1. reproducibly generated,
2. technically validated,
3. independently human-reviewed,
4. traceable to the underlying synthetic dataset.

## Data privacy

All project data are synthetic. No employer, client, patient, sponsor, proprietary, or confidential records are used.
