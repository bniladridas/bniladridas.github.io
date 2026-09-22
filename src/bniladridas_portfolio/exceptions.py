"""Typed exceptions for the bniladridas_portfolio SDK."""


class PortfolioError(Exception):
    """Base class for all portfolio SDK errors."""


class ProjectNotFoundError(PortfolioError, KeyError):
    """Raised when a project key is not present in projects.json."""


class DataNotFoundError(PortfolioError, FileNotFoundError):
    """Raised when a packaged content file is missing or invalid."""
