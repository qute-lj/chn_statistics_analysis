import json
import tempfile
import unittest
from pathlib import Path

from chn_stat.survey_pipeline import run_survey_jobs


class SurveyPipelineTests(unittest.TestCase):
    def test_run_survey_jobs_builds_summary_csv_from_config(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            raw_dir = root / "data" / "raw" / "cfps"
            raw_dir.mkdir(parents=True)
            data_path = raw_dir / "cfps_person_2020.csv"
            data_path.write_text(
                "education,wage_income\n"
                "本科,100000\n"
                "本科,120000\n"
                "硕士,150000\n",
                encoding="utf-8",
            )

            config_path = root / "cfps_config.json"
            config_path.write_text(
                json.dumps(
                    {
                        "jobs": [
                            {
                                "source": "cfps",
                                "survey_year": 2020,
                                "path": "data/raw/cfps/cfps_person_2020.csv",
                                "education_column": "education",
                                "annual_wage_column": "wage_income",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            output_path = root / "outputs" / "survey_summary.csv"

            result = run_survey_jobs(
                config_path=config_path,
                project_root=root,
                output_path=output_path,
            )

            self.assertTrue(output_path.exists())
            self.assertEqual(list(result["education_level"]), ["bachelor", "master"])
            self.assertEqual(list(result["mean_annual_wage"]), [110000.0, 150000.0])
