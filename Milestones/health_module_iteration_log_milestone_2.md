
# Health Module – Iteration Log
## Milestone 2: Historical Dataset Expansion & Longitudinal Validation

---

## v2.1 – Core biomarker selection

**Goal:** Expand beyond the MVP dataset while avoiding unnecessary complexity.

**What changed**
- Defined a focused set of ~20 core biomarkers
- Prioritised biomarkers relevant to:
  - Longevity
  - Metabolic health
  - Inflammation
  - Hormones
  - Iron status
  - Cardiovascular health
- Deliberately avoided modelling all 150+ biomarkers available from comprehensive testing

**Key learning**
- A useful health system requires representative data, not exhaustive data
- Validation should precede completeness

---

## v2.2 – Historical data backfill

**Goal:** Establish meaningful longitudinal health history.

**What changed**
- Backfilled blood test history from 2023–2026
- Added results from multiple providers:
  - NHS
  - Randox
  - OmegaQuant
- Populated historical values for key biomarkers including:
  - Vitamin D
  - B12
  - Testosterone
  - HbA1c
  - Omega-3 Index
  - Lipids
  - Iron markers
  - Thyroid markers

**Key learning**
- Longitudinal history creates significantly more value than isolated snapshots
- Trend visibility begins once multiple years of data are available

---

## v2.3 – Biomarker inventory expansion

**Goal:** Validate that the architecture scales beyond the original MVP biomarkers.

**What changed**
- Expanded tracked biomarkers from a small initial set to ~20 core biomarkers
- Added:
  - ALT
  - Ferritin
  - Iron
  - Transferrin Saturation
  - Folate
  - SHBG
  - Free Testosterone
  - TSH
  - Free T4
  - Total Cholesterol
  - LDL
  - HDL
  - Triglycerides
  - Fasting Glucose
  - HbA1c
  - hsCRP
  - Omega-3 Index

**Key learning**
- The staged architecture scaled cleanly without structural changes
- Adding biomarkers should primarily be a data exercise rather than a coding exercise

---

## v2.4 – Configuration consolidation

**Goal:** Reduce duplicated metadata and improve maintainability.

**What changed**
- Added biomarker definitions to `biomarker_ranges.csv`
- Added units, labels and KPI configuration for newly tracked biomarkers
- Removed reliance on manually maintaining unit mappings in multiple locations
- Moved closer to a single-source-of-truth configuration model

**Key learning**
- Metadata duplication creates avoidable maintenance overhead
- Configuration files should own biomarker behaviour wherever possible

"""
BIOMARKER_UNITS = {
    "Vitamin_D": "nmol/L",
    "B12": "pmol/L",
    "Testosterone": "nmol/L",
    "Omega-3 Index": "%",
}
"""

---

## v2.5 – Data validation & pipeline hardening

**Goal:** Ensure the system remains stable with a larger dataset.

**What changed**
- Resolved biomarker naming mismatches
- Resolved unit mapping issues
- Resolved dashboard build failures caused by non-numeric values
- Validated canonical output against dashboard rendering
- Verified provider traceability remained intact

**Key learning**
- Real-world data exposes architectural weaknesses faster than feature development
- Data validation is a critical part of system design

---

## v2.6 – Longitudinal dashboard validation

**Goal:** Confirm that the dashboard provides meaningful historical insight.

**What changed**
- Verified multi-year trend visualisations
- Confirmed historical timelines render correctly
- Validated KPI cards against latest results
- Confirmed latest-results table scales with expanded biomarker inventory
- Demonstrated meaningful trends such as:
  - Vitamin D decline and recovery
  - Stable HbA1c over multiple years
  - Longitudinal hormone tracking

**Key learning**
- The primary value of Health OS comes from health stories over time, not individual test results
- A functioning longitudinal dataset is more valuable than additional dashboard features

---

## Current state (Milestone 2 complete)

- 2023–2026 historical biomarker dataset
- ~20 core biomarkers tracked
- Multi-provider support validated
- Canonical longitudinal schema validated
- Config-driven biomarker metadata
- Interactive trend visualisations
- KPI cards
- Latest results table
- Provider traceability
- Stable dashboard build process
- Foundation established for health insights

---

## Explicit non-goals

- No PDF parsing
- No AI extraction
- No wearable integrations
- No databases
- No automated recommendations
- No automated interpretation

Milestone 2 prioritises data completeness, longitudinal history, and validation of the architecture before introducing insight-generation features.
