"""Frozen data models for the bniladridas_portfolio SDK."""
from dataclasses import dataclass


@dataclass(frozen=True)
class About:
    title: str
    body: str
    rule: str


@dataclass(frozen=True)
class Project:
    key: str
    name: str
    kind: str
    tagline: str
    repo_url: str
    case_study: str
    status: str
