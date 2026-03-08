from __future__ import annotations

import sys
from pathlib import Path

from chn_stat.survey_profile import render_survey_file_profile


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: uv run python scripts/profile_survey_file.py <path-to-file>")
    print(render_survey_file_profile(Path(sys.argv[1])), end="")


if __name__ == "__main__":
    main()
