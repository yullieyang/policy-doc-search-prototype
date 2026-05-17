# Data Quality Reporting and Escalation Policy

_Document ID: POL-DQ-001 · Version 2.3 · Last reviewed: 2026-03-15 · Owner: Data Governance Office_

> **Note:** This is a fictional policy document. It is not based on any
> real organization's policy, methodology, or internal procedure. It
> exists only to demonstrate how the search prototype in this
> repository handles a multi-section policy text.

## 1. Purpose and scope

This policy describes how data-quality issues identified during
recurring data refreshes are reported, triaged, and escalated. It
applies to any data product that feeds a research-support workflow,
including macro and trade indicator panels, scenario inputs, and
quarterly model-output extracts. It does not apply to ad-hoc
research-only data pulls that do not enter a versioned data product.

## 2. Definitions

- **Data-quality issue** — any observation during a refresh that the
  data does not meet the documented schema, range, or coverage
  requirements of the data product.
- **Material issue** — an issue that would change the published
  output, the downstream report, or a reviewer's decision if not
  addressed before release.
- **Owner** — the named individual or team accountable for the data
  product's documented schema and refresh cadence.

## 3. Reporting

Every data-quality issue must be reported in writing at the time of
discovery. The report contains the data product name, the refresh
date or quarter, the observed deviation, the affected fields, the
estimated row count, and the discoverer's name. Reports are stored
alongside the data product, not in a separate ticket system, so a
future reviewer reading the data product can trace the issue without
external context.

## 4. Triage

The owner triages every report within two business days. The triage
records: whether the issue is material, the immediate mitigation
(reject the refresh, hold the publication, accept with a documented
caveat), and the downstream consumers who must be informed.

## 5. Escalation

A material issue that cannot be resolved within five business days,
or that affects more than ten percent of rows in the affected data
product, is escalated to the Data Governance Office. The escalation
includes the original report, the triage record, the mitigation in
place, and a proposed resolution date.

## 6. Documentation

Every reported issue ends with a documented disposition: corrected,
accepted with caveat, or rejected with downstream re-run. The
disposition is committed to the data product's repository alongside
the affected refresh.

## 7. Out of scope

This policy does not cover model methodology issues, code defects in
the data product itself, or issues with consuming workflows. Those
are governed by separate policies (see POL-MD-001 for model
documentation, POL-CR-001 for code review).
