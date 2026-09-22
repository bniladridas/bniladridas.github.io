"""Loader for the curated about record in content/about.json.

Malformed JSON surfaces as ValueError (json.JSONDecodeError); a missing
file or a record without the required string fields raises
DataNotFoundError. Nothing here reads site HTML.
"""
import json
import pathlib

from bniladridas_portfolio.cli import get_static_dir
from bniladridas_portfolio.exceptions import DataNotFoundError
from bniladridas_portfolio.models import About

_ABOUT_RELATIVE = pathlib.Path("content") / "about.json"
_REQUIRED = ("title", "body", "rule")


def load_about(static_dir=None) -> About:
    base = pathlib.Path(static_dir) if static_dir is not None else get_static_dir()
    path = base / _ABOUT_RELATIVE
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as e:
        raise DataNotFoundError(f"About data not found: {path}") from e
    if not isinstance(raw, dict):
        raise DataNotFoundError(f"About data invalid (expected object): {path}")
    missing = [k for k in _REQUIRED if not isinstance(raw.get(k), str)]
    if missing:
        raise DataNotFoundError(f"About data missing fields {missing}: {path}")
    return About(title=raw["title"], body=raw["body"], rule=raw["rule"])
