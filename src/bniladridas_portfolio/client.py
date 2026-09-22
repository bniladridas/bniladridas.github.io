"""Read-only programmatic interface over the packaged portfolio content."""
from bniladridas_portfolio.exceptions import ProjectNotFoundError
from bniladridas_portfolio.models import About, Project
from bniladridas_portfolio.resources.about import load_about
from bniladridas_portfolio.resources.projects import load_projects


class AboutResource:
    """Read access to the curated about record."""

    def __init__(self, static_dir=None):
        self._static_dir = static_dir

    def get(self) -> About:
        return load_about(self._static_dir)


class ProjectsResource:
    """Read access to the curated project records."""

    def __init__(self, static_dir=None):
        self._static_dir = static_dir

    def list(self) -> list:
        return load_projects(self._static_dir)

    def get(self, key: str) -> Project:
        for project in load_projects(self._static_dir):
            if project.key == key:
                return project
        raise ProjectNotFoundError(key)


class Portfolio:
    """Facade over the packaged portfolio content."""

    def __init__(self, static_dir=None):
        self.about = AboutResource(static_dir)
        self.projects = ProjectsResource(static_dir)
