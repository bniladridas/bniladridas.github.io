import json
import pathlib
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bniladridas_portfolio import Portfolio
from bniladridas_portfolio.exceptions import DataNotFoundError, PortfolioError
from bniladridas_portfolio.models import About
from bniladridas_portfolio.resources.about import load_about


class TestAbout(unittest.TestCase):
    def test_get_from_checkout(self):
        about = Portfolio(static_dir=ROOT).about.get()
        self.assertIsInstance(about, About)
        self.assertTrue(about.title and about.body and about.rule)

    def test_default_portfolio_uses_checkout(self):
        self.assertEqual(Portfolio().about.get(), Portfolio(static_dir=ROOT).about.get())

    def test_missing_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(DataNotFoundError):
                load_about(pathlib.Path(tmp))

    def test_missing_file_is_file_not_found(self):
        with tempfile.TemporaryDirectory() as tmp:
            try:
                load_about(pathlib.Path(tmp))
            except DataNotFoundError as e:
                self.assertIsInstance(e, FileNotFoundError)
                self.assertIsInstance(e, PortfolioError)
            else:
                self.fail("DataNotFoundError not raised")

    def test_malformed_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            content = pathlib.Path(tmp) / "content"
            content.mkdir()
            (content / "about.json").write_text("{not json", encoding="utf-8")
            with self.assertRaises(ValueError):
                load_about(pathlib.Path(tmp))

    def test_missing_keys(self):
        with tempfile.TemporaryDirectory() as tmp:
            content = pathlib.Path(tmp) / "content"
            content.mkdir()
            (content / "about.json").write_text(json.dumps({"title": "t"}), encoding="utf-8")
            with self.assertRaises(DataNotFoundError):
                load_about(pathlib.Path(tmp))


if __name__ == "__main__":
    unittest.main()
