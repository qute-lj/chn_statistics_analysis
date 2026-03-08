import tempfile
import unittest
from pathlib import Path

from chn_stat.plotting import generate_outputs


class PlottingTests(unittest.TestCase):
    def test_generate_outputs_creates_csv_and_png(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path, png_path = generate_outputs(Path(tmpdir))
            self.assertTrue(csv_path.exists())
            self.assertTrue(png_path.exists())
