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
