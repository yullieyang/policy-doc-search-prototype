# Model Review and Approval Process

_Document ID: POL-MR-002 · Version 1.4 · Last reviewed: 2026-02-08 · Owner: Model Risk Committee_

> **Note:** This is a fictional policy document. All process steps,
> approval roles, and timelines below are illustrative. The document
> exists only as a sample for the search prototype in this
> repository.

## 1. Purpose

This policy describes the steps a model — or a material change to an
existing model — must go through before it is approved for use in
recurring research-support or risk-analytics workflows. It applies to
any model whose output is consumed by an internal decision, a
quarterly report, or a downstream dashboard.

## 2. Roles

- **Modeler** — the individual or team that developed the model.
  Owns the methodology, the calibration, and the documented
  assumptions.
- **Independent reviewer** — an analyst or modeler from outside the
  originating team. Reads the model documentation, replicates a small
  number of results, and authors the review record.
- **Approving manager** — the manager accountable for the workflow
  that consumes the model. Signs the final approval.
- **Model Risk Committee** — the standing committee that reviews
  approval records and resolves disagreements between the modeler
  and the independent reviewer.

## 3. Required documentation

Before any review begins, the modeler provides:

- A methodology note that describes the model's purpose, inputs,
  outputs, calibration choices, and identification assumptions.
- A data dictionary covering every input and output field.
- A reproducibility section: how a reviewer can re-run the model
  against a documented input and obtain the documented output.
- A statement of limitations: what the model does not do, what
  populations it is not calibrated for, and what failure modes have
  been observed.

## 4. Independent review

The independent reviewer reads the documentation, replicates at least
one documented result against the supplied input, and produces a
written review record. The review record states one of three
verdicts: approved as documented, approved with conditions (listing
each), or rejected with required follow-ups (listing each).

## 5. Approval

The approving manager reads the review record. The manager may
approve the model as reviewed, request additional information, or
defer to the Model Risk Committee. An approval is recorded with the
manager's name and the date.

## 6. Re-review

Material changes to a previously approved model — new inputs,
changes to calibration, changes to the documented output schema —
trigger a new round of independent review. Minor changes (code
refactors that do not change output, documentation clarifications)
do not.

## 7. Recordkeeping

Every approval record, review record, and supporting documentation
file is committed to the model's repository. The committee can audit
any approval by reading the repository at the corresponding commit.

## 8. Out of scope

This policy does not cover ad-hoc research models whose output is not
consumed by a recurring workflow. Those models live in the
researcher's working repository and follow the lighter-weight
guidance in POL-RS-003.
