# Health Module -- Iteration Log

## Milestone 4: Knowledge Layer & Dashboard Organisation

------------------------------------------------------------------------

## v4.1 -- Biomarker categorisation

**Goal:** Improve dashboard organisation and establish a higher-level
metadata layer for biomarkers.

**What changed** - Added a `category` field to `biomarker_ranges.csv` -
Categorised all tracked biomarkers into logical health domains
including: - Vitamins & Nutrients - Iron Status - Cardiovascular
Health - Metabolic Health - Hormones - Thyroid Function - Inflammation -
Liver Function - Minerals & Electrolytes - Fatty Acids - Updated
dashboard configuration to load category metadata directly from the
configuration file

**Key learning** - Biomarkers should belong to meaningful health domains
rather than existing as a flat list - Metadata should remain
configuration-driven rather than hardcoded into the dashboard

------------------------------------------------------------------------

## v4.2 -- Biomarker knowledge base

**Goal:** Reduce the need for external research by embedding simple
explanations directly into the dashboard.

**What changed** - Added a `description` field to
`biomarker_ranges.csv` - Introduced support for multi-line biomarker
descriptions - Added hover tooltips to biomarker names - Built the
system so descriptions are entirely configuration-driven - Validated the
feature with an initial biomarker description

**Key learning** - Users often need context before interpretation -
Separating knowledge from application logic makes the dashboard easier
to maintain and extend

------------------------------------------------------------------------

## v4.3 -- Dashboard organisation improvements

**Goal:** Improve navigation as the number of tracked biomarkers
continues to grow.

**What changed** - Grouped latest results by biomarker category - Added
collapsible category sections - Displayed biomarker counts within each
category - Reduced visual clutter while keeping all results immediately
accessible

**Key learning** - Dashboard usability becomes increasingly important as
datasets expand - Organising information often provides more value than
adding additional visualisations

------------------------------------------------------------------------

## Current state (Milestone 4 complete)

-   Config-driven biomarker categories
-   Config-driven biomarker descriptions
-   Expandable knowledge base architecture
-   Hover tooltips for biomarker explanations
-   Categorised latest-results table
-   Collapsible dashboard sections
-   Scalable metadata model
-   Stable dashboard build process

------------------------------------------------------------------------

## Explicit non-goals

-   No AI explanations
-   No automated health recommendations
-   No causal interpretation
-   No symptom analysis
-   No personalised medical advice

Milestone 4 prioritises usability, organisation, and embedded knowledge
while keeping the system deterministic, maintainable, and
configuration-driven.
