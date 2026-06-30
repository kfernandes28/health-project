# Health Module – Iteration Log
## Milestone 1: Canonical Biomarker Pipeline & Dashboard MVP

---

## v1.1 – Raw biomarker ingestion

**Goal:** Establish a simple and maintainable source of truth for blood test history.

**What changed**
- Created a raw biomarker dataset (`Raw_blood_tests.csv`)
- Supported multiple providers:
  - NHS
  - Randox
- Stored biomarker results in a human-editable wide format
- Preserved original test dates and provider attribution

**Key learning**
- Manual entry is sufficient for MVP validation
- Optimising ingestion before validating value creates unnecessary complexity

---

## v1.2 – Canonical biomarker schema

**Goal:** Decouple data entry from analysis and visualisation.

**What changed**
- Introduced canonical biomarker dataset (`biomarker_results.csv`)
- Converted wide-form blood test data into a normalized longitudinal schema
- Implemented automatic wide-to-long transformation

**Key learning**
- One row per biomarker result scales significantly better than one column per biomarker
- Canonical schemas reduce downstream complexity

---

## v1.3 – Pipeline separation

**Goal:** Separate responsibilities across the system.

**What changed**
- Established staged architecture:
  - Stage 0 – Raw
  - Stage 1 – Canonical
  - Stage 2 – Dashboard
- Introduced dedicated build scripts:
  - `build_canonical.py`
  - `build_dashboard.py`
- Dashboard now consumes only canonical data

**Key learning**
- Dashboards should never depend directly on raw data
- Stage separation improves maintainability and traceability

---

## v1.4 – Config-driven biomarker metadata

**Goal:** Move biomarker behaviour out of application code.

**What changed**
- Introduced `biomarker_ranges.csv`
- Centralised labels, units, reference ranges, optimal ranges and KPI selection
- Dashboard loads biomarker definitions dynamically

**Key learning**
- Configuration should determine behaviour wherever possible
- New biomarkers should require data changes, not code changes

---

## v1.5 – Dashboard MVP

**Goal:** Create a usable longitudinal health dashboard.

**What changed**
- Built HTML dashboard generator
- Added biomarker dropdown selector
- Added longitudinal trend chart
- Added reference range overlays
- Added provider-aware hover information

**Key learning**
- Longitudinal tracking provides more value than isolated blood test reports
- Trend visibility is the primary purpose of the health system

---

## v1.6 – KPI cards & current state view

**Goal:** Surface the most important information immediately.

**What changed**
- Added KPI cards showing latest results
- Added latest-results summary table
- Introduced config-driven KPI selection via `show_as_kpi`
- Separated headline biomarkers from the full biomarker inventory

**Key learning**
- Not all biomarkers deserve equal prominence
- Presentation priorities belong in configuration, not dashboard code

---

## v1.7 – Dashboard stability & usability

**Goal:** Improve consistency and reduce visual friction.

**What changed**
- Fixed initial dashboard render issues
- Fixed range-overlay initialisation
- Fixed dropdown state inconsistencies
- Removed redundant chart titles
- Standardised chart behaviour across biomarker selection

**Key learning**
- Small UX issues reduce trust disproportionately
- Stability matters more than additional features

---

## Current state (Milestone 1 complete)

- Raw biomarker ingestion layer
- Canonical longitudinal biomarker dataset
- Config-driven biomarker metadata
- Config-driven KPI selection
- Interactive HTML dashboard
- KPI cards
- Trend visualisation
- Latest results table
- Provider traceability
- Reusable staged architecture

---

## Explicit non-goals

- No PDF parsing
- No AI extraction
- No wearable integrations
- No databases
- No health recommendations
- No automated interpretation

Milestone 1 prioritises structure, traceability, and longitudinal visibility over automation and insight.
