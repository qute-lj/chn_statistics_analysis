import tempfile
import unittest
from pathlib import Path

from chn_stat import render_survey_input_report
from chn_stat.survey_profile import profile_survey_file, render_survey_file_profile


class SurveyInspectionTests(unittest.TestCase):
    def test_render_survey_input_report_mentions_empty_state_and_directories(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            output = render_survey_input_report(Path(tmpdir))

        self.assertIn("No survey raw files found.", output)
        self.assertIn("CFPS", output)
        self.assertIn("CHFS", output)
        self.assertIn("data/raw/cfps", output)
        self.assertIn("data/raw/chfs", output)

    def test_profile_survey_file_reports_candidate_columns_for_csv(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "cfps_person_2020.csv"
            path.write_text(
                "pid,education,wage_income,total_income,age\n"
                "1,bachelor,120000,150000,30\n"
                "2,master,180000,220000,35\n",
                encoding="utf-8",
            )

            profile = profile_survey_file(path)
            rendered = render_survey_file_profile(path)

        self.assertEqual(profile["row_count"], 2)
        self.assertEqual(profile["column_count"], 5)
        self.assertEqual(profile["survey_year"], 2020)
        self.assertIn("education", profile["candidate_columns"]["education"])
        self.assertIn("wage_income", profile["candidate_columns"]["wage"])
        self.assertIn("total_income", profile["candidate_columns"]["income"])
        self.assertIn("Candidate columns", rendered)
        self.assertIn("education", rendered)
        self.assertIn("wage_income", rendered)

    def test_profile_survey_file_rejects_unsupported_spss_reader_cleanly(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "chfs_2023.sav"
            path.write_text("fake", encoding="utf-8")

            with self.assertRaisesRegex(RuntimeError, "pyreadstat"):
                profile_survey_file(path)
