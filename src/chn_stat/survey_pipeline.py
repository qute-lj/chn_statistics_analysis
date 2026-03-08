from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

from chn_stat.survey_harmonization import aggregate_survey_wages
from chn_stat.survey_profile import load_survey_dataframe


def load_survey_job_config(config_path: Path) -> dict[str, Any]:
    with config_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def run_survey_jobs(
    *,
    config_path: Path,
    project_root: Path,
    output_path: Path | None = None,
) -> pd.DataFrame:
    payload = load_survey_job_config(config_path)
    jobs = payload.get("jobs", [])
    results: list[pd.DataFrame] = []

    for job in jobs:
        data_path = project_root / job["path"]
        frame = load_survey_dataframe(data_path)
        result = aggregate_survey_wages(
            frame,
            source=job["source"],
            survey_year=job["survey_year"],
            education_column=job["education_column"],
            annual_wage_column=job["annual_wage_column"],
            education_mapping=job.get("education_mapping"),
        )
        results.append(result)

    combined = pd.concat(results, ignore_index=True) if results else pd.DataFrame()

    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        combined.to_csv(output_path, index=False)

    return combined
