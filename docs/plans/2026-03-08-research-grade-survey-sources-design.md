# Research-Grade Survey Sources Design

## Goal

Extend the project beyond the existing proxy workflow by documenting and
preparing a research-grade path based on official survey sources:

- `CFPS`
- `CHFS`

The new path should not pretend that restricted microdata can be fetched
automatically. Instead, it should make the official sources explicit, define a
local ingestion contract, and prepare a reproducible survey-year processing
pipeline once the raw data is manually downloaded under the official terms.

## Constraints

- `CFPS` and `CHFS` both rely on official registration, data-use agreements,
  and in some cases approval or restricted-access workflows.
- The current workspace does not contain raw survey files.
- The implementation must therefore separate:
  - official source documentation
  - local input discovery and validation
  - downstream processing of user-supplied raw files
- The existing `2016-2024` proxy workflow must remain available and unchanged.

## Chosen Approach

### 1. Add a dedicated hard-source documentation page

Create a new document that records the currently reliable official source entry
points for both survey families:

- project homepages
- data application or public-data pages
- questionnaires or documentation pages
- data-use agreement or usage notice pages

The document should also explain the practical implication for this repository:
the acquisition step is manual, but everything after local placement of the
files can be automated.

### 2. Introduce a survey input contract

Define a stable on-disk layout for manually downloaded files:

- `data/raw/cfps/`
- `data/raw/chfs/`

The code should describe which file extensions are accepted and which survey
years are expected first. The first target is survey-year analysis, not annual
interpolation.

### 3. Add discovery and validation before transformation

Before attempting any income aggregation, the project should answer:

- are any raw files present?
- which source do they belong to?
- which years are represented?
- which formats are present?

This needs a lightweight inspection layer so users get a truthful status report
even when no restricted data has been placed yet.

### 4. Normalize toward a shared long-format schema

Once raw data is present, the long-term target schema is:

- `source`
- `survey_year`
- `education_level`
- `income_measure`
- `annual_wage`
- `sample_size`
- `notes`

The initial implementation does not need to solve full variable harmonization
without real files. It should create the scaffolding and fixtures needed to
support that later work cleanly.

### 5. Keep proxy and survey workflows separate

The current proxy pipeline is still useful for directional visualization. The
research-grade survey path should live alongside it instead of mutating the same
entrypoint or reusing proxy assumptions.

## Output

The implementation should deliver:

- a new documentation page for official hard sources
- updated `README` guidance explaining the proxy path vs. survey path
- a survey catalog module describing supported sources and raw-data locations
- a raw-input inspection script that reports what is locally available
- tests covering catalog metadata and local input discovery

## Verification

- unit tests for the survey catalog and discovery helpers
- a script run showing clear output when no restricted raw data exists
- regression confirmation that the existing test suite still passes

## Limitations

- This phase does not include automatic downloading of `CFPS` or `CHFS`.
- This phase does not claim a finished wage-by-education estimate from those
  surveys because the raw files are not present in the workspace.
- Actual wage harmonization across survey years will require year-specific
  variable mapping once the raw data is available.
