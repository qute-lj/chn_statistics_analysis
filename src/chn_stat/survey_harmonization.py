from __future__ import annotations

from typing import Any

import pandas as pd


EDUCATION_LEVEL_ORDER = ("college", "bachelor", "master", "doctor")

EDUCATION_ALIASES = {
    "college": (
        "college",
        "junior college",
        "associate",
        "专科",
        "大专",
    ),
    "bachelor": (
        "bachelor",
        "undergraduate",
        "本科",
        "大学本科",
    ),
    "master": (
        "master",
        "masters",
        "硕士",
        "硕士研究生",
    ),
    "doctor": (
        "doctor",
        "doctoral",
        "phd",
        "博士",
        "博士研究生",
        "博士及以上",
    ),
}


def normalize_education_level(
    value: Any,
    explicit_mapping: dict[Any, str] | None = None,
) -> str | None:
    if pd.isna(value):
        return None

    if explicit_mapping is not None and value in explicit_mapping:
        return explicit_mapping[value]

    normalized = str(value).strip().lower()
    if explicit_mapping is not None and normalized in explicit_mapping:
        return explicit_mapping[normalized]

    for level, aliases in EDUCATION_ALIASES.items():
        if any(alias in normalized for alias in aliases):
            return level
    return None


def aggregate_survey_wages(
    frame: pd.DataFrame,
    *,
    source: str,
    survey_year: int,
    education_column: str,
    annual_wage_column: str,
    education_mapping: dict[Any, str] | None = None,
) -> pd.DataFrame:
    working = frame[[education_column, annual_wage_column]].copy()
    working["education_level"] = working[education_column].map(
        lambda value: normalize_education_level(value, education_mapping)
    )
    working["annual_wage"] = pd.to_numeric(working[annual_wage_column], errors="coerce")
    working = working.dropna(subset=["education_level", "annual_wage"])
    working = working[working["annual_wage"] > 0]

    grouped = (
        working.groupby("education_level", sort=False)["annual_wage"]
        .agg(["mean", "median", "count"])
        .reset_index()
    )
    grouped = grouped.rename(
        columns={
            "mean": "mean_annual_wage",
            "median": "median_annual_wage",
            "count": "sample_size",
        }
    )

    grouped["education_level"] = pd.Categorical(
        grouped["education_level"],
        categories=EDUCATION_LEVEL_ORDER,
        ordered=True,
    )
    grouped = grouped.sort_values("education_level").reset_index(drop=True)
    grouped.insert(0, "survey_year", survey_year)
    grouped.insert(0, "source", source)
    return grouped
