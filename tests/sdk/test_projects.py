import json
import pathlib
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bniladridas_portfolio import Portfolio
from bniladridas_portfolio.exceptions import (
    DataNotFoundError,
    PortfolioError,
    ProjectNotFoundError,
)
from bniladridas_portfolio.models import Project
from bniladridas_portfolio.resources.projects import load_projects


def _write_projects(base, payload):
    content = pathlib.Path(base) / "content"
    content.mkdir(parents=True, exist_ok=True)
    (content / "projects.json").write_text(json.dumps(payload), encoding="utf-8")


class TestProjects(unittest.TestCase):
    def test_list_from_checkout(self):
        projects = Portfolio(static_dir=ROOT).projects.list()
        self.assertEqual([p.key for p in projects], ["traction", "sandbox"])
        self.assertTrue(all(isinstance(p, Project) for p in projects))

    def test_get_locked_values(self):
        sdk = Portfolio(static_dir=ROOT)
        traction = sdk.projects.get("traction")
        self.assertEqual(traction.name, "Traction: Realistic Racing Game")
        self.assertEqual(traction.repo_url, "https://github.com/bniladridas/traction")
        self.assertEqual(traction.case_study, "#traction")
        sandbox = sdk.projects.get("sandbox")
        self.assertEqual(sandbox.name, "Palmshed Sandbox: Secure Runtime")
        self.assertEqual(sandbox.repo_url, "https://github.com/palmshed/sandbox")
        self.assertEqual(sandbox.status, "Stable · v1.2.0 (Sep 2026)")

    def test_unknown_key(self):
        try:
            Portfolio(static_dir=ROOT).projects.get("nope")
        except ProjectNotFoundError as e:
            self.assertIsInstance(e, KeyError)
            self.assertIsInstance(e, PortfolioError)
        else:
            self.fail("ProjectNotFoundError not raised")

    def test_missing_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(DataNotFoundError):
                load_projects(pathlib.Path(tmp))

    def test_malformed_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            content = pathlib.Path(tmp) / "content"
            content.mkdir(parents=True)
            (content / "projects.json").write_text("{not json", encoding="utf-8")
            with self.assertRaises(ValueError):
                load_projects(pathlib.Path(tmp))

    def test_record_missing_key(self):
        with tempfile.TemporaryDirectory() as tmp:
            _write_projects(tmp, {"projects": [{"key": "x"}]})
            with self.assertRaises(DataNotFoundError):
                load_projects(pathlib.Path(tmp))

    def test_not_a_list(self):
        with tempfile.TemporaryDirectory() as tmp:
            _write_projects(tmp, {"projects": {"key": "x"}})
            with self.assertRaises(DataNotFoundError):
                load_projects(pathlib.Path(tmp))


if __name__ == "__main__":
    unittest.main()
