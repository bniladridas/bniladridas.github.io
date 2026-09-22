"""Loader for the curated project records in content/projects.json.

This is the only data source for project records. It never falls back to
parsing site HTML. Malformed JSON surfaces as ValueError
(json.JSONDecodeError); a missing file or records without the required
string fields raise DataNotFoundError.
"""
import json
import pathlib

from bniladridas_portfolio.cli import get_static_dir
from bniladridas_portfolio.exceptions import DataNotFoundError
from bniladridas_portfolio.models import Project

_PROJECTS_RELATIVE = pathlib.Path("content") / "projects.json"
_REQUIRED = ("key", "name", "kind", "tagline", "repo_url", "case_study", "status")


def load_projects(static_dir=None) -> list:
    base = pathlib.Path(static_dir) if static_dir is not None else get_static_dir()
    path = base / _PROJECTS_RELATIVE
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as e:
        raise DataNotFoundError(f"Projects data not found: {path}") from e
    if not isinstance(raw, dict) or not isinstance(raw.get("projects"), list):
        raise DataNotFoundError(f"Projects data invalid (expected object with projects list): {path}")
    projects = []
    for i, record in enumerate(raw["projects"]):
        if not isinstance(record, dict):
            raise DataNotFoundError(f"Projects data invalid at index {i}: {path}")
        missing = [k for k in _REQUIRED if not isinstance(record.get(k), str)]
        if missing:
            raise DataNotFoundError(f"Projects data missing fields {missing} at index {i}: {path}")
        projects.append(Project(**{k: record[k] for k in _REQUIRED}))
    return projects
