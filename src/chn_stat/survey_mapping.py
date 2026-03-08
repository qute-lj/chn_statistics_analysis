from __future__ import annotations

from pathlib import Path
from typing import Any

from chn_stat.survey_profile import profile_survey_file


def _pick_first(values: list[str]) -> str | None:
    return values[0] if values else None


def suggest_survey_job(path: Path, *, source: str, project_root: Path) -> dict[str, Any]:
    profile = profile_survey_file(path)
    try:
        serialized_path = path.relative_to(project_root).as_posix()
    except ValueError:
        serialized_path = str(path)
    candidates = profile["candidate_columns"]

    annual_wage_column = _pick_first(candidates["wage"]) or _pick_first(candidates["income"])

    return {
        "source": source,
        "survey_year": profile["survey_year"],
        "path": serialized_path,
        "education_column": _pick_first(candidates["education"]),
        "annual_wage_column": annual_wage_column,
        "education_mapping": {},
    }
