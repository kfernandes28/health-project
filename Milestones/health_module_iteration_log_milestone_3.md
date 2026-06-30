# Health Module – Iteration Log
## Milestone 3: Context Layer & Insight Generation

---

## v3.1 – Intervention Tracking System

**Goal:** Add context to biomarker trends by linking health interventions to longitudinal data.

**What changed**
- Created `interventions.csv`
- Created `intervention_biomarker_links.csv`
- Introduced intervention start and end date tracking
- Added support for linking a single intervention to multiple biomarkers
- Added intervention timeline markers to biomarker charts
- Added intervention annotations to visualisations

**Key learning**
- Biomarker data becomes significantly more useful when viewed in the context of actions taken
- The system should track what happened, not attempt to determine why it happened

---

## v3.2 – Multi-biomarker intervention validation

**Goal:** Validate that interventions can be reused across multiple biomarkers.

**What changed**
- Added Calcium to the tracked biomarker inventory
- Linked Vitamin D supplementation to both Vitamin D and Calcium
- Validated that a single intervention renders correctly across multiple biomarker views
- Confirmed intervention architecture scales without dashboard changes

**Key learning**
- Interventions should exist independently from biomarkers
- Relationships should be configuration-driven rather than hardcoded

---

## v3.3 – Change Detection Engine

**Goal:** Surface meaningful changes between consecutive tests.

**What changed**
- Added previous-result lookup logic
- Calculated absolute change between latest and previous result
- Calculated percentage change
- Added change detection to latest-results table
- Added colour-coded increase/decrease indicators
- Handled first-result scenarios gracefully

**Key learning**
- Users naturally ask "What changed?" before asking for deeper analysis
- Comparing results manually across reports creates unnecessary friction

---

## v3.4 – Status Classification Engine

**Goal:** Provide an immediate understanding of current biomarker state.

**What changed**
- Introduced automatic status classification:
  - Low
  - Normal
  - Optimal
  - High
- Built config-driven status calculation using `biomarker_ranges.csv`
- Added colour-coded status indicators to latest-results table
- Ensured biomarker behaviour remains controlled through configuration rather than code

**Key learning**
- Status logic should be data-driven and configurable
- Range definitions and application logic should remain separate concerns

---

## v3.5 – Dashboard usability improvements

**Goal:** Improve the speed at which health insights can be extracted.

**What changed**
- Enhanced latest-results table with:
  - Previous value
  - Change value
  - Percentage change
  - Status
- Improved visual hierarchy through colour coding
- Reduced need to manually compare historical blood test reports
- Improved dashboard usefulness immediately after receiving new test results

**Key learning**
- The value of a dashboard comes from reducing effort required to answer common questions
- Insight generation is often a presentation problem rather than a data problem

---

## Current state (Milestone 3 complete)

- Historical biomarker tracking
- Config-driven biomarker metadata
- KPI cards
- Latest-results table
- Status engine
- Change detection engine
- Intervention tracking system
- Multi-biomarker intervention linking
- Timeline annotations
- Range overlays
- Interactive trend visualisations
- Provider traceability
- Stable staged architecture

---

## Explicit non-goals

- No PDF parsing
- No AI extraction
- No wearable integrations
- No databases
- No automated recommendations
- No causal health interpretation

Milestone 3 prioritises context, change awareness, and insight generation while remaining deterministic, explainable, and configuration-driven.
