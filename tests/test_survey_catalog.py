import tempfile
import unittest
from pathlib import Path

from chn_stat.survey_catalog import get_survey_catalog
from chn_stat.survey_inputs import build_survey_input_report, discover_survey_files


class SurveyCatalogTests(unittest.TestCase):
    def test_catalog_contains_cfps_and_chfs(self) -> None:
        catalog = get_survey_catalog()

        self.assertEqual(set(catalog.keys()), {"cfps", "chfs"})
        for source in catalog.values():
            self.assertTrue(source.raw_dir)
            self.assertTrue(source.official_urls)
            self.assertTrue(source.preferred_years)

    def test_discover_survey_files_finds_supported_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            cfps_dir = root / "data" / "raw" / "cfps"
            chfs_dir = root / "data" / "raw" / "chfs"
            cfps_dir.mkdir(parents=True)
            chfs_dir.mkdir(parents=True)

            (cfps_dir / "cfps_person_2018.dta").write_text("fake", encoding="utf-8")
            (chfs_dir / "chfs_household_2021.csv").write_text("fake", encoding="utf-8")
            (chfs_dir / "ignore.me").write_text("fake", encoding="utf-8")

            discovered = discover_survey_files(root)

        self.assertEqual(len(discovered), 2)
        self.assertEqual(discovered[0].source, "cfps")
        self.assertEqual(discovered[0].survey_year, 2018)
        self.assertEqual(discovered[0].extension, ".dta")
        self.assertEqual(discovered[1].source, "chfs")
        self.assertEqual(discovered[1].survey_year, 2021)
        self.assertEqual(discovered[1].extension, ".csv")

    def test_build_survey_input_report_handles_missing_directories(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            report = build_survey_input_report(Path(tmpdir))

        self.assertEqual(report["total_files"], 0)
        self.assertEqual(set(report["sources"].keys()), {"cfps", "chfs"})
        self.assertFalse(report["sources"]["cfps"]["exists"])
        self.assertFalse(report["sources"]["chfs"]["exists"])
