import tempfile
import unittest
from pathlib import Path

import pandas as pd

from chn_stat.survey_plotting import generate_survey_year_outputs


class SurveyPlottingTests(unittest.TestCase):
    def test_generate_survey_year_outputs_creates_csv_and_png(self) -> None:
        frame = pd.DataFrame(
            [
                {
                    "source": "cfps",
                    "survey_year": 2020,
                    "education_level": "college",
                    "mean_annual_wage": 80000.0,
                    "median_annual_wage": 80000.0,
                    "sample_size": 10,
                },
                {
                    "source": "cfps",
                    "survey_year": 2020,
                    "education_level": "bachelor",
                    "mean_annual_wage": 110000.0,
                    "median_annual_wage": 110000.0,
                    "sample_size": 20,
                },
                {
                    "source": "cfps",
                    "survey_year": 2022,
                    "education_level": "college",
                    "mean_annual_wage": 85000.0,
                    "median_annual_wage": 84000.0,
                    "sample_size": 11,
                },
                {
                    "source": "cfps",
                    "survey_year": 2022,
                    "education_level": "bachelor",
                    "mean_annual_wage": 118000.0,
                    "median_annual_wage": 117000.0,
                    "sample_size": 21,
                },
            ]
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path, png_path = generate_survey_year_outputs(
                frame,
                Path(tmpdir),
                stem="cfps_survey_year_summary",
            )

            self.assertTrue(csv_path.exists())
            self.assertTrue(png_path.exists())
