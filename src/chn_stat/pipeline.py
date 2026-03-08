from __future__ import annotations

import json
from pathlib import Path
from statistics import mean
from typing import Any

import pandas as pd


DATA_DIR = Path(__file__).resolve().parent / "data"
BASELINE_REFERENCE_YEAR = 2024


def _load_json(filename: str) -> dict[str, Any]:
    with (DATA_DIR / filename).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_official_wages() -> dict[int, dict[str, Any]]:
    payload = _load_json("official_wages.json")
    return {entry["year"]: entry for entry in payload["years"]}


def load_education_proxy() -> dict[str, Any]:
    return _load_json("education_proxy_2024.json")


def calibrate_blend_weight(official_wages: dict[int, dict[str, Any]]) -> float:
    numerator = 0.0
    denominator = 0.0
    for entry in official_wages.values():
        enterprise = entry.get("scale_above_enterprise")
        if not enterprise:
            continue
        non_private = entry["non_private"]["value"]
        private = entry["private"]["value"]
        target = enterprise["value"] - private
        delta = non_private - private
        numerator += delta * target
        denominator += delta * delta
    if denominator == 0:
        raise ValueError("No calibration points were found for the synthetic baseline.")
    weight = numerator / denominator
    return max(0.0, min(1.0, weight))


def compute_reference_factors(proxy_payload: dict[str, Any]) -> dict[str, float]:
    levels = proxy_payload["education_levels"]
    bachelor_average = mean(levels["bachelor"]["salaries"].values())
    return {
        key: mean(level["salaries"].values()) / bachelor_average
        for key, level in levels.items()
    }


def _dispersion_scale(
    year_entry: dict[str, Any],
    reference_entry: dict[str, Any],
) -> float:
    year_gap = year_entry["non_private"]["value"] / year_entry["private"]["value"] - 1.0
    reference_gap = (
        reference_entry["non_private"]["value"] / reference_entry["private"]["value"] - 1.0
    )
    if reference_gap <= 0:
        return 1.0
    return year_gap / reference_gap


def _scale_factor(reference_factor: float, gap_scale: float) -> float:
    if reference_factor >= 1.0:
        return 1.0 + (reference_factor - 1.0) * gap_scale
    return 1.0 - (1.0 - reference_factor) * gap_scale


def build_proxy_salary_series() -> pd.DataFrame:
    official_wages = load_official_wages()
    proxy_payload = load_education_proxy()

    blend_weight = calibrate_blend_weight(official_wages)
    reference_factors = compute_reference_factors(proxy_payload)
    reference_entry = official_wages[BASELINE_REFERENCE_YEAR]

    rows: list[dict[str, Any]] = []
    for year in sorted(official_wages):
        entry = official_wages[year]
        non_private = entry["non_private"]["value"]
        private = entry["private"]["value"]
        synthetic_baseline = round(private + blend_weight * (non_private - private), 2)
        gap_scale = _dispersion_scale(entry, reference_entry)

        college_factor = _scale_factor(reference_factors["college"], gap_scale)
        bachelor_factor = _scale_factor(reference_factors["bachelor"], gap_scale)
        master_factor = _scale_factor(reference_factors["master"], gap_scale)
        doctor_factor = _scale_factor(reference_factors["doctor"], gap_scale)

        rows.append(
            {
                "year": year,
                "official_non_private": non_private,
                "official_private": private,
                "synthetic_baseline": synthetic_baseline,
                "college": round(synthetic_baseline * college_factor, 2),
                "bachelor": round(synthetic_baseline * bachelor_factor, 2),
                "master": round(synthetic_baseline * master_factor, 2),
                "doctor": round(synthetic_baseline * doctor_factor, 2),
            }
        )

    return pd.DataFrame(rows)
