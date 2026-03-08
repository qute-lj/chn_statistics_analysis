from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from chn_stat.survey_catalog import REPO_ROOT, SurveySource, get_survey_catalog


YEAR_PATTERN = re.compile(r"(?<!\d)(19\d{2}|20\d{2})(?!\d)")


@dataclass(frozen=True)
class DiscoveredSurveyFile:
    source: str
    name: str
    path: Path
    extension: str
    survey_year: int | None


def _resolve_raw_dir(project_root: Path, source: SurveySource) -> Path:
    return project_root / source.raw_dir


def infer_survey_year(filename: str) -> int | None:
    match = YEAR_PATTERN.search(filename)
    if match is None:
        return None
    return int(match.group(1))


def discover_survey_files(project_root: Path = REPO_ROOT) -> list[DiscoveredSurveyFile]:
    catalog = get_survey_catalog()
    discovered: list[DiscoveredSurveyFile] = []

    for source in catalog.values():
        raw_dir = _resolve_raw_dir(project_root, source)
        if not raw_dir.exists():
            continue
        for path in sorted(raw_dir.rglob("*")):
            if not path.is_file():
                continue
            extension = path.suffix.lower()
            if extension not in source.accepted_extensions:
                continue
            discovered.append(
                DiscoveredSurveyFile(
                    source=source.slug,
                    name=path.name,
                    path=path,
                    extension=extension,
                    survey_year=infer_survey_year(path.name),
                )
            )

    return sorted(
        discovered,
        key=lambda item: (item.source, item.survey_year or 0, item.name.lower()),
    )


def build_survey_input_report(project_root: Path = REPO_ROOT) -> dict[str, object]:
    catalog = get_survey_catalog()
    discovered = discover_survey_files(project_root)
    by_source: dict[str, list[DiscoveredSurveyFile]] = {slug: [] for slug in catalog}
    for item in discovered:
        by_source[item.source].append(item)

    sources: dict[str, dict[str, object]] = {}
    for slug, source in catalog.items():
        raw_dir = _resolve_raw_dir(project_root, source)
        items = by_source[slug]
        years = sorted({item.survey_year for item in items if item.survey_year is not None})
        sources[slug] = {
            "name": source.name,
            "raw_dir": source.raw_dir.as_posix(),
            "exists": raw_dir.exists(),
            "accepted_extensions": list(source.accepted_extensions),
            "preferred_years": list(source.preferred_years),
            "official_urls": list(source.official_urls),
            "file_count": len(items),
            "survey_years": years,
            "files": [
                {
                    "name": item.name,
                    "extension": item.extension,
                    "survey_year": item.survey_year,
                    "path": str(item.path),
                }
                for item in items
            ],
        }

    return {
        "project_root": str(project_root),
        "total_files": len(discovered),
        "sources": sources,
    }


def render_survey_input_report(project_root: Path = REPO_ROOT) -> str:
    report = build_survey_input_report(project_root)
    lines = [
        "Research-grade survey input inspection",
        f"Project root: {report['project_root']}",
        "",
    ]
    if report["total_files"] == 0:
        lines.append("No survey raw files found.")
        lines.append(
            "Next step: download approved CFPS/CHFS files and place them in the "
            "configured raw-data directories."
        )
        lines.append("")

    for slug, entry in report["sources"].items():
        name = str(entry["name"])
        raw_dir = str(entry["raw_dir"])
        exists = "yes" if entry["exists"] else "no"
        years = entry["survey_years"]
        year_text = ", ".join(str(year) for year in years) if years else "none"

        lines.extend(
            [
                f"{name} ({slug})",
                f"  raw_dir: {raw_dir}",
                f"  exists: {exists}",
                f"  accepted_extensions: {', '.join(entry['accepted_extensions'])}",
                f"  preferred_years: {', '.join(str(year) for year in entry['preferred_years'])}",
                f"  discovered_files: {entry['file_count']}",
                f"  discovered_years: {year_text}",
            ]
        )

        files = entry["files"]
        if files:
            lines.append("  files:")
            for item in files:
                year = item["survey_year"] if item["survey_year"] is not None else "unknown"
                lines.append(f"    - {item['name']} (year={year}, ext={item['extension']})")

        lines.append("")

    return "\n".join(lines).rstrip() + "\n"
