# chn-stat

Generate a proxy wage trend chart for China from `2016` through `2024` for:

- `大专`
- `本科`
- `硕士研究生`
- `博士研究生`

## Why this is a proxy

AkShare does not currently expose a direct annual national series for "average wage
by education level", and the live NBS easyquery interface returned a JavaScript
challenge during implementation. The project therefore uses:

- official NBS yearly wage bulletins for the main wage backbone
- a public 2024 salary report for education-level spacing

This is suitable for visualization and directional comparison, not for claiming
exact official NBS wage levels by education.

## Data sources and proxy index

### Data sources actually used

1. Official NBS annual wage bulletins for `2016-2024`
   - `城镇非私营单位就业人员年平均工资`
   - `城镇私营单位就业人员年平均工资`
   - saved locally in `src/chn_stat/data/official_wages.json`

2. The `2023` and `2024` combined NBS wage bulletins also publish
   `规模以上企业就业人员年平均工资`
   - `2023`: `98096`
   - `2024`: `102452`
   - these two values are used only to calibrate the blend weight between the
     private and non-private official wage series

3. A public `2024` salary report preview page for education spacing
   - saved locally in `src/chn_stat/data/education_proxy_2024.json`
   - source page:
     `https://max.book118.com/html/2024/0707/7032001101006131.shtm`
   - used only for relative education-level spacing, not as a direct official
     workforce wage source

### How the wage relative index is built

The implementation uses three steps.

Step 1: build the synthetic baseline wage

```text
synthetic_baseline_t = w * non_private_t + (1 - w) * private_t
```

where:

- `non_private_t` = official NBS non-private average wage in year `t`
- `private_t` = official NBS private average wage in year `t`
- `w = 0.5866989301513226`

This `w` is estimated from the `2023` and `2024` NBS bulletins so the blended
series tracks the published `规模以上企业就业人员年平均工资`.

Step 2: compute the education reference factors from the public 2024 table

The report provides a salary table by education level and company type. The code
averages across company types, then normalizes by `本科 = 1.0`.

Reference factors:

- `大专`: `0.881597414196402`
- `本科`: `1.0`
- `硕士研究生`: `1.2801003700080806`
- `博士研究生`: `1.962786543614171`

Step 3: scale the education gap by yearly official wage dispersion

```text
gap_scale_t =
((non_private_t / private_t) - 1) /
((non_private_2024 / private_2024) - 1)
```

Then the yearly factor for each education group is:

```text
if reference_factor >= 1:
    factor_t = 1 + (reference_factor - 1) * gap_scale_t
else:
    factor_t = 1 - (1 - reference_factor) * gap_scale_t
```

Finally:

```text
education_wage_t = synthetic_baseline_t * factor_t
```

This means the chart's yearly movement is anchored to official NBS wage changes,
while the spacing between education groups is anchored to the public 2024
education salary table.

## Commands

Generate the CSV and PNG:

```bash
uv run chn-stat
```

Equivalent script entry:

```bash
uv run python scripts/generate_education_wage_proxy.py
```

Print the generated yearly series to the terminal:

```bash
uv run python scripts/print_proxy_series.py
```

Print the saved source URLs:

```bash
uv run python scripts/show_proxy_sources.py
```

Run tests:

```bash
uv run python -m unittest discover -s tests -v
```

## Outputs

Generated files are written to `outputs/`:

- `education_wage_proxy_2016_2024.csv`
- `education_wage_proxy_2016_2024.png`
