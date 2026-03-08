import tempfile
import unittest
from pathlib import Path

from chn_stat.survey_mapping import suggest_survey_job


class SurveyMappingTests(unittest.TestCase):
    def test_suggest_survey_job_uses_candidate_columns_from_profile(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            path = root / "data" / "raw" / "cfps" / "cfps_person_2020.csv"
            path.parent.mkdir(parents=True)
            path.write_text(
                "education,wage_income,total_income\n"
                "本科,100000,120000\n",
                encoding="utf-8",
            )

            suggestion = suggest_survey_job(path, source="cfps", project_root=root)

        self.assertEqual(suggestion["source"], "cfps")
        self.assertEqual(suggestion["survey_year"], 2020)
        self.assertEqual(suggestion["path"], "data/raw/cfps/cfps_person_2020.csv")
        self.assertEqual(suggestion["education_column"], "education")
        self.assertEqual(suggestion["annual_wage_column"], "wage_income")

    def test_suggest_survey_job_falls_back_to_absolute_path_outside_project_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir) / "repo"
            root.mkdir()
            external = Path(tmpdir) / "external.csv"
            external.write_text(
                "education,wage_income\n本科,100000\n",
                encoding="utf-8",
            )

            suggestion = suggest_survey_job(external, source="cfps", project_root=root)

        self.assertEqual(suggestion["path"], str(external))
