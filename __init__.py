"""A3 package public API.

Re-exports commonly used classes and functions so external imports like
`from A3 import Project, ProjectManager, create_enhanced_project` continue to work.
"""

from .models import (
    Project,
    CurrentProject,
    PastProject,
    Location,
    Organization,
    EnhancedProject,
    EnhancedCurrentProject,
    EnhancedPastProject,
)
from .exceptions import (
    InvalidChoiceException,
    InvalidCategoryException,
    InvalidStateException,
    InvalidCityException,
    InvalidYearException,
    InvalidStatusException,
    InvalidReportTypeException,
    InvalidBudgetException,
    InvalidDateException,
    InvalidStateAddressException,
)
from .manager import ProjectManager
from .visualization import VisualizationDecorator
from .reporting import generate_summary_report
from .cli import create_enhanced_project, main

__all__ = [
    # models
    "Project",
    "CurrentProject",
    "PastProject",
    "Location",
    "Organization",
    "EnhancedProject",
    "EnhancedCurrentProject",
    "EnhancedPastProject",
    # exceptions
    "InvalidChoiceException",
    "InvalidCategoryException",
    "InvalidStateException",
    "InvalidCityException",
    "InvalidYearException",
    "InvalidStatusException",
    "InvalidReportTypeException",
    "InvalidBudgetException",
    "InvalidDateException",
    "InvalidStateAddressException",
    # manager/visualization
    "ProjectManager",
    "VisualizationDecorator",
    # functions
    "generate_summary_report",
    "create_enhanced_project",
    "main",
]
