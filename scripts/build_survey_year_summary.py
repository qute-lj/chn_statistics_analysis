from __future__ import annotations

import sys
from pathlib import Path

from chn_stat.survey_pipeline import run_survey_jobs
from chn_stat.survey_plotting import generate_survey_year_outputs


def main() -> None:
    if len(sys.argv) not in {2, 3}:
        raise SystemExit(
            "Usage: uv run python scripts/build_survey_year_summary.py "
            "<config-path> [output-csv]"
        )

    config_path = Path(sys.argv[1])
    output_path = (
        Path(sys.argv[2])
        if len(sys.argv) == 3
        else Path.cwd() / "outputs" / f"{config_path.stem}.csv"
    )
    frame = run_survey_jobs(
        config_path=config_path,
        project_root=Path.cwd(),
        output_path=output_path,
    )
    csv_path, png_path = generate_survey_year_outputs(
        frame,
        output_path.parent,
        stem=output_path.stem,
    )
    print(f"Rows written: {len(frame)}")
    print(f"CSV written to: {csv_path}")
    print(f"PNG written to: {png_path}")


if __name__ == "__main__":
    main()
