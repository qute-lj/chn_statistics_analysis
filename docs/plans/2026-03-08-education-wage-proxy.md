# Education Wage Proxy Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a reproducible pipeline that generates a `2016-2024` China wage trend chart for `大专` / `本科` / `硕士研究生` / `博士研究生` using an official wage backbone plus a documented education-level proxy.

**Architecture:** Store the official yearly wage inputs and education calibration inputs as versioned local data files, transform them into a synthetic yearly series in pure Python, and render a chart plus CSV from a small CLI entrypoint. Keep the proxy formula explicit and tested so the result is reproducible and reviewable.

**Tech Stack:** Python 3.12, uv, pandas, matplotlib, unittest

---

### Task 1: Add local source data files

**Files:**
- Create: `src/chn_stat/data/official_wages.json`
- Create: `src/chn_stat/data/education_proxy_2024.json`

**Step 1: Write the failing test**

```python
def test_source_data_has_expected_year_range(self):
    data = load_official_wages()
    self.assertEqual(min(data.keys()), 2016)
    self.assertEqual(max(data.keys()), 2024)
```

**Step 2: Run test to verify it fails**

Run: `uv run python -m unittest tests.test_pipeline -v`
Expected: FAIL because loader function and data files do not exist.

**Step 3: Write minimal implementation**

- Add the two JSON files with:
  - yearly official non-private/private wage values and source URLs
  - 2024 education calibration table and source URL

**Step 4: Run test to verify it passes**

Run: `uv run python -m unittest tests.test_pipeline -v`
Expected: PASS for the source-range test.

**Step 5: Commit**

Skip commit because this workspace is not a git repository.

### Task 2: Build the transformation layer

**Files:**
- Create: `src/chn_stat/pipeline.py`
- Test: `tests/test_pipeline.py`

**Step 1: Write the failing test**

```python
def test_build_proxy_series_returns_expected_columns(self):
    df = build_proxy_salary_series()
    self.assertEqual(
        list(df.columns),
        [
            "year",
            "official_non_private",
            "official_private",
            "synthetic_baseline",
            "college",
            "bachelor",
            "master",
            "doctor",
        ],
    )
```

**Step 2: Run test to verify it fails**

Run: `uv run python -m unittest tests.test_pipeline -v`
Expected: FAIL because `build_proxy_salary_series` does not exist.

**Step 3: Write minimal implementation**

- Load the local JSON files
- Compute the synthetic baseline
- Compute normalized education multipliers
- Scale yearly multipliers by official non-private/private dispersion
- Return a tidy pandas DataFrame

**Step 4: Run test to verify it passes**

Run: `uv run python -m unittest tests.test_pipeline -v`
Expected: PASS for the shape/columns test.

**Step 5: Commit**

Skip commit because this workspace is not a git repository.

### Task 3: Lock behavior with ordering and calibration tests

**Files:**
- Modify: `tests/test_pipeline.py`

**Step 1: Write the failing test**

```python
def test_education_levels_stay_ordered(self):
    df = build_proxy_salary_series()
    for _, row in df.iterrows():
        self.assertLess(row["college"], row["bachelor"])
        self.assertLess(row["bachelor"], row["master"])
        self.assertLess(row["master"], row["doctor"])
```

**Step 2: Run test to verify it fails**

Run: `uv run python -m unittest tests.test_pipeline -v`
Expected: FAIL if the proxy scaling is wrong.

**Step 3: Write minimal implementation**

- Adjust multiplier logic so the ordering is guaranteed
- Add a calibration helper for the baseline blend weight

**Step 4: Run test to verify it passes**

Run: `uv run python -m unittest tests.test_pipeline -v`
Expected: PASS.

**Step 5: Commit**

Skip commit because this workspace is not a git repository.

### Task 4: Add plotting and CLI output

**Files:**
- Create: `src/chn_stat/plotting.py`
- Modify: `src/chn_stat/__init__.py`
- Create: `tests/test_plotting.py`

**Step 1: Write the failing test**

```python
def test_generate_outputs_creates_csv_and_png(self):
    with tempfile.TemporaryDirectory() as tmpdir:
        csv_path, png_path = generate_outputs(Path(tmpdir))
        self.assertTrue(csv_path.exists())
        self.assertTrue(png_path.exists())
```

**Step 2: Run test to verify it fails**

Run: `uv run python -m unittest tests.test_plotting -v`
Expected: FAIL because output generation does not exist.

**Step 3: Write minimal implementation**

- Add chart rendering with Chinese labels
- Add CSV export
- Update `main()` so `uv run chn-stat` writes outputs to `outputs/`

**Step 4: Run test to verify it passes**

Run: `uv run python -m unittest tests.test_plotting -v`
Expected: PASS.

**Step 5: Commit**

Skip commit because this workspace is not a git repository.

### Task 5: End-to-end verification

**Files:**
- Modify if needed after verification: `src/chn_stat/*.py`

**Step 1: Write the failing test**

No new test. Use the existing automated tests as the regression suite.

**Step 2: Run test to verify it fails**

Not applicable.

**Step 3: Write minimal implementation**

- Fix any issues revealed by end-to-end execution
- Ensure chart annotation includes approximation caveat

**Step 4: Run test to verify it passes**

Run: `uv run python -m unittest -v`
Run: `uv run chn-stat`
Expected:
- all tests PASS
- `outputs/education_wage_proxy_2016_2024.csv` exists
- `outputs/education_wage_proxy_2016_2024.png` exists

**Step 5: Commit**

Skip commit because this workspace is not a git repository.
