from __future__ import annotations

import json
import sys
from pathlib import Path

from chn_stat.survey_mapping import suggest_survey_job


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit(
            "Usage: uv run python scripts/suggest_survey_job.py <source> <path-to-file>"
        )

    source = sys.argv[1]
    path = Path(sys.argv[2]).resolve()
    print(json.dumps(suggest_survey_job(path, source=source, project_root=Path.cwd()), indent=2))


if __name__ == "__main__":
    main()
