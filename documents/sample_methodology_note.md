# Model Documentation Expectations — Methodology Note

_Document ID: MTH-DOC-005 · Version 3.1 · Last reviewed: 2026-04-02 · Owner: Methodology Working Group_

> **Note:** This is a fictional methodology note. The standards
> described below are illustrative and are not based on any real
> organization's documentation policy. The note exists only as a
> sample for the search prototype in this repository.

## 1. Purpose

This note describes the minimum documentation a model author must
produce before the model is submitted for independent review under
POL-MR-002 (Model Review and Approval Process). The note is a
checklist of expected sections, not a template; the model author
chooses the format that suits the model and the audience, as long as
every expected section is present.

## 2. Expected sections

### 2.1 Purpose

A two-to-four sentence statement of what the model is for and which
recurring workflow consumes it.

### 2.2 Inputs

A list of every input series, table, or file. For each input:

- Source (vendor, internal system, public API).
- Frequency (daily, monthly, quarterly, ad-hoc).
- Units, sign conventions, and seasonal-adjustment status where
  applicable.
- Documented schema or column list.
- Vintage or revision policy.

Inputs that the model accepts but does not require should be marked
as optional with the default behavior described.

### 2.3 Transformations

The transformations applied between input and output, in the order
they occur. For each transformation:

- Mathematical formula or precise prose specification.
- The assumption it depends on (base year, deflator, lag length,
  identification choice).
- The artifact or function in the codebase that implements it.

### 2.4 Outputs

A list of every output artifact. For each output:

- Path or destination.
- Schema, with column-level dtype and validation rules.
- Update cadence.
- Retention policy.

### 2.5 Reproducibility

A reproducibility section describes how a reviewer re-runs the model
against a documented input and obtains the documented output. At
minimum:

- The exact command that runs the model end-to-end.
- The pinned environment (e.g. `renv.lock`, `requirements.txt`).
- The location of the canonical input fixture used for documentation.
- Any random seed the model fixes.

### 2.6 Limitations

The limitations section describes what the model does not do, what
populations it is not calibrated for, and what failure modes have
been observed. The section is required, not optional. A model
without a written limitations section is not eligible for review.

### 2.7 Out-of-scope items

A short list of things the model could be extended to do but
deliberately does not. This section reduces over-interpretation by
downstream consumers.

## 3. Versioning

Material methodology changes (new inputs, calibration changes, new
identification assumptions) trigger a version bump in the
methodology note. Minor changes (typo fixes, prose tightening) do
not.

## 4. Audience

The methodology note is written for an independent reviewer who has
not seen the model before. A reviewer with the relevant domain
training should be able to replicate one documented result from the
note alone, without follow-up.
