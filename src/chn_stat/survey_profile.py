from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from chn_stat.survey_inputs import infer_survey_year


CANDIDATE_KEYWORDS = {
    "education": ("education", "edu", "degree", "school", "学历", "受教育"),
    "wage": ("wage", "salary", "pay", "earn", "工资", "薪资", "薪酬"),
    "income": ("income", "earnings", "收入", "所得"),
    "employment": ("employment", "employ", "job", "work", "occupation", "职业", "工作", "就业"),
}


def load_survey_dataframe(path: Path) -> pd.DataFrame:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(path)
    if suffix == ".dta":
        return pd.read_stata(path)
    if suffix in {".xlsx", ".xls"}:
        return pd.read_excel(path)
    if suffix == ".sav":
        try:
            import pyreadstat  # noqa: F401
        except ModuleNotFoundError as exc:
            raise RuntimeError("pyreadstat is required to read SPSS .sav files.") from exc
        return pd.read_spss(path)
    raise ValueError(f"Unsupported survey file type: {suffix}")


def _find_candidate_columns(columns: list[str]) -> dict[str, list[str]]:
    candidates: dict[str, list[str]] = {}
    for group, keywords in CANDIDATE_KEYWORDS.items():
        matched = []
        for column in columns:
            normalized = column.lower()
            if any(keyword in normalized for keyword in keywords):
                matched.append(column)
        candidates[group] = matched
    return candidates


def profile_survey_file(path: Path) -> dict[str, Any]:
    frame = load_survey_dataframe(path)
    columns = [str(column) for column in frame.columns]
    return {
        "file_path": str(path),
        "extension": path.suffix.lower(),
        "survey_year": infer_survey_year(path.name),
        "row_count": int(len(frame)),
        "column_count": len(columns),
        "columns": [{"name": name, "dtype": str(frame[name].dtype)} for name in columns],
        "candidate_columns": _find_candidate_columns(columns),
    }


def render_survey_file_profile(path: Path) -> str:
    profile = profile_survey_file(path)
    lines = [
        "Survey file profile",
        f"File: {profile['file_path']}",
        f"Extension: {profile['extension']}",
        f"Survey year: {profile['survey_year']}",
        f"Rows: {profile['row_count']}",
        f"Columns: {profile['column_count']}",
        "",
        "Candidate columns",
    ]

    for group, columns in profile["candidate_columns"].items():
        text = ", ".join(columns) if columns else "none"
        lines.append(f"  {group}: {text}")

    lines.append("")
    lines.append("All columns")
    for column in profile["columns"]:
        lines.append(f"  {column['name']}: {column['dtype']}")

    return "\n".join(lines).rstrip() + "\n"
