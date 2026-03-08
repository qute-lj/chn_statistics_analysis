# Education Wage Proxy Design

## Goal

Generate a China salary trend chart for `2016-2024` with four education groups:
`大专`, `本科`, `硕士研究生`, `博士研究生`.

Because AkShare does not expose a direct national "average wage by education level"
series, the chart will use a documented proxy:

- Official annual wage backbone from the National Bureau of Statistics (NBS)
- Education-level separation calibrated from a public salary report
- A transparent formula to map the backbone into four education-level series

`2025` is excluded because the official 2025 annual wage bulletin had not been
released as of `2026-03-08`.

## Constraints

- AkShare's NBS easyquery interface is currently blocked by a JavaScript challenge,
  so it cannot be used directly for this series in this environment.
- The project should still use AkShare where possible, but official public NBS
  bulletin pages are the stable source for the yearly wage backbone.
- The requested metric is "all employed people by education level", but no direct
  official annual series is exposed through AkShare or the public NBS tree that was
  inspected. The result must therefore be labeled as an approximation.

## Chosen Approach

### 1. Official wage backbone

Use the official NBS annual average wage bulletins for:

- `城镇非私营单位就业人员年平均工资`
- `城镇私营单位就业人员年平均工资`

for each year from `2016` through `2024`.

Create a synthetic baseline wage for "employed persons" by blending the two
official series:

`synthetic_baseline = w * non_private + (1 - w) * private`

where `w` is calibrated from the `2023` and `2024` official bulletins so the blend
tracks the published `规模以上企业就业人员年平均工资` level.

### 2. Education proxy factors

Use a public `2024` graduate salary report page that exposes a by-education salary
table:

- `博士及以上`
- `硕士`
- `本科`
- `专科`

The report provides salary values by company type. The implementation will average
across company types to obtain one calibration level per education group, then
normalize those levels against `本科 = 1.0`.

These normalized factors are not treated as direct workforce wages. They are used
only to determine the relative spacing between education groups.

### 3. Time-varying proxy spread

Using a fixed education multiplier would create four parallel lines. To make the
 proxy reflect changing labor-market dispersion without inventing new data, the
education spread will be scaled each year by the official gap between non-private
and private wages:

- larger official private/non-private dispersion -> wider education gap
- smaller official private/non-private dispersion -> narrower education gap

This keeps all time variation anchored to official yearly wage data.

### 4. Relative index details

The final implementation uses these explicit quantities:

- blend weight: `w = 0.5866989301513226`
- 2024 reference factors:
  - `大专 = 0.881597414196402`
  - `本科 = 1.0`
  - `硕士研究生 = 1.2801003700080806`
  - `博士研究生 = 1.962786543614171`

For each year `t`:

- `synthetic_baseline_t = w * non_private_t + (1 - w) * private_t`
- `gap_scale_t = ((non_private_t / private_t) - 1) / ((non_private_2024 / private_2024) - 1)`
- the yearly education factor is scaled from the 2024 reference factor by `gap_scale_t`
- the yearly proxy wage is `synthetic_baseline_t * factor_t`

## Output

The implementation will generate:

- a CSV with the yearly proxy wage series
- a PNG line chart

The chart will clearly state that it is an approximation and summarize the proxy
construction in a caption/footer.

## Verification

- Unit tests for the data transformation pipeline
- A file-generation test for the plot output
- A CLI run that produces the CSV and PNG successfully

## Limitations

- This is not an official NBS "wage by education level" table.
- The education factors are calibrated from a public salary report that is closer
  to recruitment-market compensation than to a full-population wage microdataset.
- The result is suitable for directional comparison and visualization, not for
  claiming exact official wage levels by education.
