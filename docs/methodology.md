# Methodology

## Data sources

### 1. Official National Bureau of Statistics wage bulletins

The backbone of the series comes from official NBS annual wage bulletins for:

- `城镇非私营单位就业人员年平均工资`
- `城镇私营单位就业人员年平均工资`

for each year from `2016` to `2024`.

These values and source URLs are saved in:

- `src/chn_stat/data/official_wages.json`

For `2023` and `2024`, the same official combined bulletins also publish:

- `规模以上企业就业人员年平均工资`

Those two published values are:

- `2023`: `98096`
- `2024`: `102452`

They are used only to estimate the blend weight for the synthetic baseline.

### 2. Public education-spacing source

The education gap comes from a public preview page of a `2024` salary report:

- `https://max.book118.com/html/2024/0707/7032001101006131.shtm`

This source is not treated as an official workforce wage table. It is used only
to calibrate the relative spacing between:

- `大专`
- `本科`
- `硕士研究生`
- `博士研究生`

The extracted values are stored in:

- `src/chn_stat/data/education_proxy_2024.json`

## Why AkShare is not the final live source

AkShare was inspected and tested during implementation, but the live NBS
easyquery path returned a JavaScript challenge in this environment, so it was not
reliable enough for a reproducible pipeline. The final project therefore uses
saved official bulletin values plus a saved public proxy table.

## Wage relative index construction

### Step 1: synthetic baseline

For each year `t`, build a synthetic baseline wage:

```text
synthetic_baseline_t = w * non_private_t + (1 - w) * private_t
```

where:

- `non_private_t` is the official non-private annual average wage
- `private_t` is the official private annual average wage
- `w = 0.5866989301513226`

The weight `w` is fit from the `2023` and `2024` NBS bulletins so the blended
series tracks the published `规模以上企业就业人员年平均工资`.

### Step 2: 2024 education reference factors

The 2024 public salary table is averaged across company types and normalized to
`本科 = 1.0`.

Reference factors:

- `大专`: `0.881597414196402`
- `本科`: `1.0`
- `硕士研究生`: `1.2801003700080806`
- `博士研究生`: `1.962786543614171`

### Step 3: yearly gap scaling

The education gap is widened or narrowed each year using the official yearly gap
between non-private and private wages:

```text
gap_scale_t =
((non_private_t / private_t) - 1) /
((non_private_2024 / private_2024) - 1)
```

Then for each education group:

```text
if reference_factor >= 1:
    factor_t = 1 + (reference_factor - 1) * gap_scale_t
else:
    factor_t = 1 - (1 - reference_factor) * gap_scale_t
```

### Step 4: yearly proxy wage series

The yearly proxy wage is:

```text
education_wage_t = synthetic_baseline_t * factor_t
```

## Interpretation

- The chart is a proxy, not a direct official NBS table by education level.
- The time trend is driven by official wage bulletins.
- The education spread is driven by a saved 2024 public salary table.
- `2025` is excluded because the official `2025` annual wage bulletin had not
  been released as of `2026-03-08`.
