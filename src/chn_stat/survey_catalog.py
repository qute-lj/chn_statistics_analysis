from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class SurveySource:
    slug: str
    name: str
    raw_dir: Path
    accepted_extensions: tuple[str, ...]
    preferred_years: tuple[int, ...]
    official_urls: tuple[str, ...]
    notes: str


def get_survey_catalog() -> dict[str, SurveySource]:
    return {
        "cfps": SurveySource(
            slug="cfps",
            name="CFPS",
            raw_dir=Path("data/raw/cfps"),
            accepted_extensions=(".dta", ".sav", ".csv", ".xlsx", ".xls"),
            preferred_years=(2016, 2018, 2020, 2022),
            official_urls=(
                "https://www.isss.pku.edu.cn/cfps/",
                "https://www.isss.pku.edu.cn/cfps/sjzx/gksj/index.htm",
                "https://www.isss.pku.edu.cn/cfps/en/data/DataUserAgreement/index.htm",
                "https://www.isss.pku.edu.cn/cfps/en/documentation/questionnaires/index.htm",
            ),
            notes=(
                "CFPS is a research-grade panel source. Data acquisition remains "
                "manual under the official access workflow."
            ),
        ),
        "chfs": SurveySource(
            slug="chfs",
            name="CHFS",
            raw_dir=Path("data/raw/chfs"),
            accepted_extensions=(".dta", ".sav", ".csv", ".xlsx", ".xls"),
            preferred_years=(2017, 2019, 2021, 2023),
            official_urls=(
                "https://chfs.swufe.edu.cn/",
                "https://chfs.swufe.edu.cn/info/1041/2131.htm",
                "https://chfs.swufe.edu.cn/info/1041/3981.htm",
                "https://chfs.swufe.edu.cn/info/1041/3931.htm",
            ),
            notes=(
                "CHFS is a research-grade income and household-finance source. "
                "Data acquisition remains manual under the official access workflow."
            ),
        ),
    }
