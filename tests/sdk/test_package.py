import pathlib
import re
import shutil
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

import bniladridas_portfolio
from bniladridas_portfolio import (
    DataNotFoundError,
    Portfolio,
    PortfolioError,
    ProjectNotFoundError,
)


class TestPackage(unittest.TestCase):
    def test_version_unchanged(self):
        declared = re.search(r'^version = "([^"]+)"', (ROOT / "pyproject.toml").read_text(), re.M).group(1)
        self.assertEqual(bniladridas_portfolio.__version__, declared)

    def test_exception_inheritance(self):
        self.assertTrue(issubclass(PortfolioError, Exception))
        self.assertTrue(issubclass(ProjectNotFoundError, (PortfolioError, KeyError)))
        self.assertTrue(issubclass(DataNotFoundError, (PortfolioError, FileNotFoundError)))

    def test_installed_style_tree(self):
        with tempfile.TemporaryDirectory() as tmp:
            static = pathlib.Path(tmp) / "static" / "content"
            static.mkdir(parents=True)
            for name in ("about.json", "projects.json"):
                shutil.copy(ROOT / "content" / name, static / name)
            installed = Portfolio(static_dir=pathlib.Path(tmp) / "static")
            checkout = Portfolio(static_dir=ROOT)
            self.assertEqual(installed.about.get(), checkout.about.get())
            self.assertEqual(installed.projects.list(), checkout.projects.list())

    def test_public_exports(self):
        for name in ("About", "DataNotFoundError", "Portfolio", "PortfolioError", "Project", "ProjectNotFoundError"):
            self.assertIn(name, bniladridas_portfolio.__all__)
            self.assertTrue(hasattr(bniladridas_portfolio, name))


if __name__ == "__main__":
    unittest.main()
