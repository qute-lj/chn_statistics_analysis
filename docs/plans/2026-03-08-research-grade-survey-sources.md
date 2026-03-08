# Research-Grade Survey Sources Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Document official CFPS/CHFS hard sources and add a local ingestion scaffold for survey-year processing.

**Architecture:** Keep the existing proxy pipeline unchanged. Add a separate survey metadata and input-discovery layer that documents official sources, defines local raw-data directories, and reports which CFPS/CHFS files are available before any restricted-data processing begins.

**Tech Stack:** Python 3.12, pathlib, json, unittest, uv

---

### Task 1: Document hard sources and workflow boundaries

**Files:**
- Create: `docs/hard-data-sources.md`
- Modify: `README.md`

**Step 1: Write the failing expectation**

Review the repository and note the missing documentation gap:
- there is no single page for official `CFPS` and `CHFS` source links
- `README.md` does not distinguish the proxy workflow from the research-grade survey workflow

**Step 2: Verify the gap**

Run: `rg -n "CFPS|CHFS|hard source|survey-year" README.md docs`
Expected: existing matches are incomplete or absent for the new workflow

**Step 3: Write minimal documentation**

Create `docs/hard-data-sources.md` with:
- official `CFPS` source links
- official `CHFS` source links
- access constraints
- recommended first-wave years for analysis
- repository placement rules for manually downloaded files

Update `README.md` with:
- a new section that points to the hard-source doc
- a short explanation of proxy path vs. survey path

**Step 4: Verify the documentation is present**

Run: `rg -n "CFPS|CHFS|survey-year|data/raw/cfps|data/raw/chfs" README.md docs/hard-data-sources.md`
Expected: all new sections are present

### Task 2: Add survey source catalog metadata

**Files:**
- Create: `src/chn_stat/survey_catalog.py`
- Test: `tests/test_survey_catalog.py`

**Step 1: Write the failing test**

Add tests that assert:
- both `cfps` and `chfs` are present in the catalog
- each source exposes a raw-data directory
- each source exposes at least one official URL
- each source exposes preferred starting survey years

**Step 2: Run test to verify it fails**

Run: `uv run python -m unittest tests.test_survey_catalog -v`
Expected: FAIL because `survey_catalog.py` does not exist yet

**Step 3: Write minimal implementation**

Implement a small metadata module that returns structured source definitions for:
- name
- slug
- raw_dir
- accepted extensions
- preferred survey years
- official URLs
- notes

**Step 4: Run test to verify it passes**

Run: `uv run python -m unittest tests.test_survey_catalog -v`
Expected: PASS

### Task 3: Add raw-input discovery helpers

**Files:**
- Create: `src/chn_stat/survey_inputs.py`
- Modify: `tests/test_survey_catalog.py`

**Step 1: Write the failing test**

Add tests that:
- build a temporary project-like directory
- place fake `cfps` and `chfs` raw files in the configured directories
- assert discovery reports the right source, path, extension, and survey year when present
- assert missing directories produce an empty but valid report

**Step 2: Run test to verify it fails**

Run: `uv run python -m unittest tests.test_survey_catalog -v`
Expected: FAIL because discovery helpers are missing

**Step 3: Write minimal implementation**

Implement helpers that:
- resolve each source raw directory relative to the repository root
- scan supported extensions
- infer a likely survey year from filenames when digits are present
- return a normalized list of discovered files

**Step 4: Run test to verify it passes**

Run: `uv run python -m unittest tests.test_survey_catalog -v`
Expected: PASS

### Task 4: Add a user-facing inspection script

**Files:**
- Create: `scripts/inspect_survey_inputs.py`
- Modify: `pyproject.toml`
- Modify: `src/chn_stat/__init__.py`
- Test: `tests/test_survey_inspection.py`

**Step 1: Write the failing test**

Add a test that runs the inspection entrypoint against an empty workspace fixture
and asserts the output clearly reports:
- no raw files found
- which directories were checked
- which sources are supported

**Step 2: Run test to verify it fails**

Run: `uv run python -m unittest tests.test_survey_inspection -v`
Expected: FAIL because the inspection entrypoint does not exist

**Step 3: Write minimal implementation**

Add an inspection function and script that prints:
- supported sources
- raw directories
- accepted extensions
- discovered file counts
- next-step guidance for manually downloaded datasets

If no files exist, it should exit successfully with an honest message instead of
pretending the survey pipeline is ready.

**Step 4: Run test to verify it passes**

Run: `uv run python -m unittest tests.test_survey_inspection -v`
Expected: PASS

### Task 5: Run full verification

**Files:**
- Verify only

**Step 1: Run targeted tests**

Run: `uv run python -m unittest tests.test_survey_catalog tests.test_survey_inspection -v`
Expected: all targeted tests pass

**Step 2: Run existing full suite**

Run: `uv run python -m unittest discover -s tests -v`
Expected: full suite passes, including existing proxy tests

**Step 3: Run the inspection command**

Run: `uv run python scripts/inspect_survey_inputs.py`
Expected: clear empty-state status unless restricted raw files have been added

**Step 4: Commit**

```bash
git add README.md docs/hard-data-sources.md docs/plans/2026-03-08-research-grade-survey-sources-design.md docs/plans/2026-03-08-research-grade-survey-sources.md src/chn_stat/survey_catalog.py src/chn_stat/survey_inputs.py src/chn_stat/__init__.py scripts/inspect_survey_inputs.py tests/test_survey_catalog.py tests/test_survey_inspection.py pyproject.toml
git commit -m "feat: scaffold research-grade survey source workflow"
```
