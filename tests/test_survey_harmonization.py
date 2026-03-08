import unittest

import pandas as pd

from chn_stat.survey_harmonization import (
    aggregate_survey_wages,
    normalize_education_level,
)


class SurveyHarmonizationTests(unittest.TestCase):
    def test_normalize_education_level_handles_common_aliases(self) -> None:
        self.assertEqual(normalize_education_level("大专"), "college")
        self.assertEqual(normalize_education_level("本科"), "bachelor")
        self.assertEqual(normalize_education_level("硕士研究生"), "master")
        self.assertEqual(normalize_education_level("PhD"), "doctor")

    def test_normalize_education_level_uses_explicit_mapping_for_codes(self) -> None:
        mapping = {1: "college", 2: "bachelor", 3: "master", 4: "doctor"}

        self.assertEqual(normalize_education_level(1, mapping), "college")
        self.assertEqual(normalize_education_level(4, mapping), "doctor")
        self.assertIsNone(normalize_education_level(9, mapping))

    def test_aggregate_survey_wages_groups_by_target_education_levels(self) -> None:
        frame = pd.DataFrame(
            [
                {"edu": "大专", "annual_wage": 80000},
                {"edu": "本科", "annual_wage": 100000},
                {"edu": "本科", "annual_wage": 120000},
                {"edu": "硕士", "annual_wage": 150000},
                {"edu": "博士", "annual_wage": 220000},
                {"edu": "未知", "annual_wage": 999999},
                {"edu": "本科", "annual_wage": -1},
            ]
        )

        result = aggregate_survey_wages(
            frame,
            source="cfps",
            survey_year=2020,
            education_column="edu",
            annual_wage_column="annual_wage",
        )

        self.assertEqual(
            list(result["education_level"]),
            ["college", "bachelor", "master", "doctor"],
        )
        self.assertEqual(list(result["sample_size"]), [1, 2, 1, 1])
        self.assertEqual(list(result["mean_annual_wage"]), [80000.0, 110000.0, 150000.0, 220000.0])
