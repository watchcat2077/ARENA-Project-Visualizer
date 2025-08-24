from typing import List

from .exceptions import InvalidBudgetException, InvalidDateException


class Project:
    projects: List["Project"] = []

    def __init__(self, name: str, category: str, year_started: str, location):
        self.__name = name
        self.__category = category
        self.__year_started = year_started
        self.__location = location
        self.__organization = []
        self.__total_cost = 0
        self.__funding = 0

    def __str__(self):
        return f"""
    Project info: 
    Name: {self.__name},
    Category: {self.__category},
    Year Started: {self.__year_started},
    Location: {self.__location},
    Funding: {self.__funding},
    Total Cost: {self.__total_cost}
"""

    @staticmethod
    def print_all_projects():
        if not Project.projects:
            print("No projects available.")
        else:
            for project in Project.projects:
                print(project)

    def add_to_list(self):
        Project.projects.append(self)

    @staticmethod
    def search_by_name(name):
        for p in Project.projects:
            if p.get_name() == name:
                return p
        return None

    @staticmethod
    def write_project_to_file(filename):
        try:
            with open(filename, 'w') as file:
                for project in Project.projects:
                    file.write(str(project))
                    file.write("\n")
            print(f"Projects have been successfully written to {filename}")
        except IOError as e:
            print(f"An I/O error occurred: {e}")

    @staticmethod
    def load_projects_from_file(filename):
        try:
            with open(filename, 'r') as file:
                project_data = {}
                for line in file:
                    line = line.strip()
                    if line:
                        if line.startswith("Project info"):
                            continue  # skip the header
                        if ": " in line:
                            key, value = line.split(": ", 1)
                            project_data[key.strip().rstrip(',')] = value.strip().rstrip(',')
                    else:
                        if project_data:
                            # Create location object
                            location_str = project_data.get('Location', '')
                            if ', ' in location_str:
                                city, state = location_str.split(', ', 1)
                                location = Location(state, city)
                            else:
                                location = Location("Unknown", location_str)

                            project = Project(
                                project_data.get('Name'),
                                project_data.get('Category'),
                                project_data.get('Year Started'),
                                location
                            )
                            # Handle funding/cost
                            if 'Funding' in project_data:
                                try:
                                    project.set_funding(float(project_data['Funding']))
                                except ValueError:
                                    pass
                            if 'Total Cost' in project_data:
                                try:
                                    project.set_total_cost(float(project_data['Total Cost']))
                                except ValueError:
                                    pass
                            Project.projects.append(project)
                            project_data = {}

                # Add last project if file doesn't end with a blank line
                if project_data:
                    location_str = project_data.get('Location', '')
                    if ', ' in location_str:
                        city, state = location_str.split(', ', 1)
                        location = Location(state, city)
                    else:
                        location = Location("Unknown", location_str)

                    project = Project(
                        project_data.get('Name'),
                        project_data.get('Category'),
                        project_data.get('Year Started'),
                        location
                    )
                    if 'Funding' in project_data:
                        try:
                            project.set_funding(float(project_data['Funding']))
                        except ValueError:
                            pass
                    if 'Total Cost' in project_data:
                        try:
                            project.set_total_cost(float(project_data['Total Cost']))
                        except ValueError:
                            pass
                    Project.projects.append(project)
            print(f"Projects successfully loaded from {filename}")
        except FileNotFoundError:
            print(f"File {filename} not found.")
        except Exception as e:
            print(f"An error occurred while loading projects: {e}")

    def get_name(self):
        return self.__name

    def get_category(self):
        return self.__category

    def set_category(self, category):
        self.__category = category

    def get_year_started(self):
        return f"Year Started: {self.__year_started}"

    def set_year_started(self, year):
        self.__year_started = year

    def get_location(self):
        return str(self.__location)

    def set_location(self, location):
        self.__location = location

    def set_total_cost(self, total_cost):
        self.__total_cost = total_cost

    def get_total_cost(self):
        return f"Total Cost: {self.__total_cost}"

    def set_funding(self, funding):
        self.__funding = funding

    def get_funding(self):
        return f"Funding: {self.__funding}"

    def add_organization(self, organization):
        self.__organization.append(organization)

    # Internal helpers for derived classes/utilities (avoid name-mangling from outside)
    def _get_year_started_value(self) -> str:
        return self.__year_started

    def _get_total_cost_value(self) -> float:
        return self.__total_cost

    def _get_funding_value(self) -> float:
        return self.__funding

    def _get_location_obj(self):
        return self.__location


class CurrentProject(Project):
    def __init__(self, name: str, category: str, year_started: str, location):
        super().__init__(name, category, year_started, location)
        self.__status = "Current"


class PastProject(Project):
    def __init__(self, name: str, category: str, year_started: str, location):
        super().__init__(name, category, year_started, location)
        self.__status = "Past"


class Location:
    def __init__(self, state, city):
        self.__state = state
        self.__city = city

    def __str__(self):
        return f"{self.__city}, {self.__state}"

    def get_state(self):
        return self.__state


class Organization:
    def __init__(self, name):
        self.__name = name
        self.__involved_projects = []


class EnhancedProject(Project):
    def __init__(self, name: str, category: str, year_started: str, location,
                 budget: str = "", project_period: str = ""):
        super().__init__(name, category, year_started, location)
        self.__budget = budget
        self.__project_period = project_period

    def set_budget(self, budget: str):
        InvalidBudgetException.validate_budget(budget)
        self.__budget = budget

    def get_budget(self):
        return self.__budget

    def set_project_period(self, period: str):
        InvalidDateException.validate_date_range(period)
        self.__project_period = period

    def get_project_period(self):
        return self.__project_period

    def to_dict(self):
        """Convert project to dictionary for JSON serialization"""
        return {
            'name': self.get_name(),
            'category': self.get_category(),
            'year_started': self._get_year_started_value(),
            'location': str(self.get_location()),
            'total_cost': self._get_total_cost_value(),
            'funding': self._get_funding_value(),
            'budget': self.__budget,
            'project_period': self.__project_period,
            'type': self.__class__.__name__,
        }

    @classmethod
    def from_dict(cls, data):
        """Create project from dictionary for JSON deserialization"""
        location_parts = data['location'].split(', ')
        if len(location_parts) >= 2:
            city = location_parts[0]
            state = location_parts[1]
            location = Location(state, city)
        else:
            location = Location("Unknown", data['location'])

        project_type = data.get('type', 'EnhancedProject')

        if project_type == 'EnhancedCurrentProject':
            project = EnhancedCurrentProject(
                data['name'], data['category'],
                data['year_started'], location,
                data.get('budget', ''), data.get('project_period', '')
            )
        elif project_type == 'EnhancedPastProject':
            project = EnhancedPastProject(
                data['name'], data['category'],
                data['year_started'], location,
                data.get('budget', ''), data.get('project_period', '')
            )
        else:
            project = cls(
                data['name'], data['category'],
                data['year_started'], location,
                data.get('budget', ''), data.get('project_period', '')
            )

        project.set_total_cost(data.get('total_cost', 0))
        project.set_funding(data.get('funding', 0))

        return project


class EnhancedCurrentProject(EnhancedProject, CurrentProject):
    def __init__(self, name: str, category: str, year_started: str, location,
                 budget: str = "", project_period: str = ""):
        EnhancedProject.__init__(self, name, category, year_started, location, budget, project_period)
        CurrentProject.__init__(self, name, category, year_started, location)


class EnhancedPastProject(EnhancedProject, PastProject):
    def __init__(self, name: str, category: str, year_started: str, location,
                 budget: str = "", project_period: str = ""):
        EnhancedProject.__init__(self, name, category, year_started, location, budget, project_period)
        PastProject.__init__(self, name, category, year_started, location)
