from __future__ import annotations

from pathlib import Path

from chn_stat.plotting import generate_outputs
from chn_stat.survey_inputs import render_survey_input_report


def main() -> None:
    output_dir = Path.cwd() / "outputs"
    csv_path, png_path = generate_outputs(output_dir)
    print(f"CSV written to: {csv_path}")
    print(f"PNG written to: {png_path}")


def inspect_survey_inputs_cli() -> None:
    print(render_survey_input_report(Path.cwd()), end="")
