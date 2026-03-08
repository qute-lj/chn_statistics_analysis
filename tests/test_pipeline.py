import unittest

from chn_stat.pipeline import build_proxy_salary_series, load_official_wages


class PipelineTests(unittest.TestCase):
    def test_source_data_has_expected_year_range(self) -> None:
        data = load_official_wages()
        self.assertEqual(min(data.keys()), 2016)
        self.assertEqual(max(data.keys()), 2024)

    def test_build_proxy_series_returns_expected_columns(self) -> None:
        frame = build_proxy_salary_series()
        self.assertEqual(
            list(frame.columns),
            [
                "year",
                "official_non_private",
                "official_private",
                "synthetic_baseline",
                "college",
                "bachelor",
                "master",
                "doctor",
            ],
        )

    def test_education_levels_stay_ordered(self) -> None:
        frame = build_proxy_salary_series()
        for row in frame.itertuples(index=False):
            self.assertLess(row.college, row.bachelor)
            self.assertLess(row.bachelor, row.master)
            self.assertLess(row.master, row.doctor)
