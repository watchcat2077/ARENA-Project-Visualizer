import json
import re
import matplotlib.pyplot as plt
from datetime import datetime


class Project:
    projects = []
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

class InvalidChoiceException(Exception):
    @staticmethod
    def validate_choice(choice):
        if choice not in ['1', '2', '3', '4', '5', 'x', 'X']:
            raise InvalidChoiceException(f"Invalid choice: {choice}")

class InvalidCategoryException(Exception):
    valid_category = ["Bioenergy", "Energy from waste", "Battery storage", "Solar energy", "Distributed energy resources", "Electric vehicles", "Wind energy", "Education"]

    @staticmethod
    def validate_category(category):
        if category not in InvalidCategoryException.valid_category:
            raise InvalidCategoryException(f"Invalid category: {category}")

class InvalidStateException(Exception):
    valid_state = ["Australian Capital Territory", "National", "New South Wales", "Northern Territory", "Queensland", "South Australia", "Tasmania", "Victoria", "Western Australia"]

    @staticmethod
    def validate_state(state):
        if state not in InvalidStateException.valid_state:
            raise InvalidStateException(f"Invalid state: {state}")

class InvalidCityException(Exception):
    valid_city = [
        "Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide",
        "Canberra", "Hobart", "Darwin", "Gold Coast", "Newcastle",
        "Wollongong", "Geelong", "Townsville", "Cairns", "Toowoomba",
        "Ballarat", "Bendigo", "Launceston", "Mackay", "Rockhampton"
    ]

    @staticmethod
    def validate_city(city):
        if city not in InvalidCityException.valid_city:
            raise InvalidCityException(f"Invalid city: {city}")

class InvalidYearException(Exception):
    valid_year = [str(year) for year in range(2009, 2026)]

    @staticmethod
    def validate_year(year):
        if year not in InvalidYearException.valid_year:
            raise InvalidYearException(f"Invalid year: {year}")

class InvalidStatusException(Exception):
    @staticmethod
    def validate_status(status):
        if status not in ["Current", "Past"]:
            raise InvalidStatusException(f"Invalid status: {status}")

class InvalidReportTypeException(Exception):
    @staticmethod
    def validate_type(type):
        if type not in ["1", "2", "category", "state"]:
            raise InvalidReportTypeException(f"Invalid report type: {type}")

class InvalidBudgetException(Exception):
    @staticmethod
    def validate_budget(budget_str):
        pattern = r'^\$\d+(\.\d{2})?[mk]$'
        if not re.match(pattern, budget_str, re.IGNORECASE):
            raise InvalidBudgetException(f"Invalid budget format: {budget_str}. Use format like $4.81m or $500k")

class InvalidDateException(Exception):
    @staticmethod
    def validate_date_range(date_range):
        # Pattern for date range: DD/MM/YYYY – DD/MM/YYYY (accepts both - and –)
        pattern = r'^\d{2}/\d{2}/\d{4}\s*[–-]\s*\d{2}/\d{2}/\d{4}$'
        if not re.match(pattern, date_range):
            raise InvalidDateException(f"Invalid date format: {date_range}. Use format: DD/MM/YYYY – DD/MM/YYYY")
        
        # Validate actual dates - handle both dash types
        try:
            # Split on either type of dash
            if '–' in date_range:
                dates = date_range.split('–')
            else:
                dates = date_range.split('-')
            
            start_date_str = dates[0].strip()
            end_date_str = dates[1].strip()
            
            # Validate date format more strictly
            if not re.match(r'^\d{2}/\d{2}/\d{4}$', start_date_str) or not re.match(r'^\d{2}/\d{2}/\d{4}$', end_date_str):
                raise InvalidDateException(f"Invalid date format in: {date_range}")
            
            start_date = datetime.strptime(start_date_str, '%d/%m/%Y')
            end_date = datetime.strptime(end_date_str, '%d/%m/%Y')
            
            if start_date >= end_date:
                raise InvalidDateException("Start date must be before end date")
                
        except ValueError as e:
            raise InvalidDateException(f"Invalid date values in: {date_range}")

class InvalidStateAddressException(Exception):
    valid_states = [
        "Australian Capital Territory", "National", "New South Wales", 
        "Northern Territory", "Queensland", "South Australia", 
        "Tasmania", "Victoria", "Western Australia"
    ]
    
    @staticmethod
    def validate_state_address(address):
        # Check if any valid state is in the address
        for state in InvalidStateAddressException.valid_states:
            if state in address:
                return
        raise InvalidStateAddressException(f"Invalid state address: {address}")

# Enhanced Project class with JSON serialization
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
            'year_started': self._Project__year_started,
            'location': str(self.get_location()),
            'total_cost': self._Project__total_cost,
            'funding': self._Project__funding,
            'budget': self.__budget,
            'project_period': self.__project_period,
            'type': self.__class__.__name__
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
        
        # Import here to avoid circular imports
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

# Singleton pattern for project manager
class ProjectManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ProjectManager, cls).__new__(cls)
            cls._instance.projects = []
        return cls._instance
    
    def load_from_json(self, filename="ARENA_projects.JSON"):
        """Load projects from JSON file"""
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                self.projects = []
                for project_data in data:
                    project = EnhancedProject.from_dict(project_data)
                    self.projects.append(project)
                Project.projects = self.projects
            print(f"Projects successfully loaded from {filename}")
            return True
        except FileNotFoundError:
            print(f"JSON file {filename} not found. Will load from text file.")
            return False
        except Exception as e:
            print(f"Error loading from JSON: {e}")
            return False
    
    def save_to_json(self, filename="ARENA_projects.JSON"):
        """Save projects to JSON file"""
        try:
            data = [project.to_dict() for project in self.projects]
            with open(filename, 'w') as file:
                json.dump(data, file, indent=2)
            print(f"Projects successfully saved to {filename}")
        except Exception as e:
            print(f"Error saving to JSON: {e}")
    
    def import_from_text(self, filename="ARENA_projects.txt"):
        """Import projects from text file and convert to enhanced projects"""
        Project.load_projects_from_file(filename)
        enhanced_projects = []
        for project in Project.projects:
            enhanced_project = EnhancedProject(
                project.get_name(),
                project.get_category(),
                project._Project__year_started,
                project._Project__location
            )
            enhanced_project.set_total_cost(project._Project__total_cost)
            enhanced_project.set_funding(project._Project__funding)
            enhanced_projects.append(enhanced_project)
        
        self.projects = enhanced_projects
        Project.projects = self.projects

# Visualization class using decorator pattern
class VisualizationDecorator:
    def __init__(self, projects):
        self.projects = projects
    
    def generate_bar_chart(self, title, filename):
        """Generate bar chart for project categories"""
        categories = {}
        for project in self.projects:
            cat = project.get_category()
            categories[cat] = categories.get(cat, 0) + 1
        
        plt.figure(figsize=(12, 6))
        plt.bar(categories.keys(), categories.values())
        plt.title(f'{title} - Projects by Category')
        plt.xlabel('Category')
        plt.ylabel('Number of Projects')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(f'{filename}_bar_chart.png')
        plt.show()
        print(f"Bar chart saved as {filename}_bar_chart.png")
    
    def generate_pie_chart(self, title, filename):
        """Generate pie chart for funding distribution"""
        total_funding = {}
        for project in self.projects:
            cat = project.get_category()
            funding = project._Project__funding if hasattr(project, '_Project__funding') else 0
            total_funding[cat] = total_funding.get(cat, 0) + funding
        
        # Filter out categories with zero funding
        filtered_funding = {k: v for k, v in total_funding.items() if v > 0}
        
        if not filtered_funding:
            # If no funding data, show project count instead
            categories = {}
            for project in self.projects:
                cat = project.get_category()
                categories[cat] = categories.get(cat, 0) + 1
            filtered_funding = categories
        
        plt.figure(figsize=(10, 8))
        plt.pie(filtered_funding.values(), labels=filtered_funding.keys(), autopct='%1.1f%%')
        plt.title(f'{title} - Funding Distribution by Category')
        plt.tight_layout()
        plt.savefig(f'{filename}_pie_chart.png')
        plt.show()
        print(f"Pie chart saved as {filename}_pie_chart.png")
    
    def generate_line_chart(self, title, filename):
        """Generate line chart for projects over years"""
        years = {}
        for project in self.projects:
            year = project._Project__year_started
            years[year] = years.get(year, 0) + 1
        
        sorted_years = sorted(years.items())
        
        plt.figure(figsize=(10, 6))
        plt.plot([item[0] for item in sorted_years], [item[1] for item in sorted_years], marker='o')
        plt.title(f'{title} - Projects Started by Year')
        plt.xlabel('Year')
        plt.ylabel('Number of Projects')
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(f'{filename}_line_chart.png')
        plt.show()
        print(f"Line chart saved as {filename}_line_chart.png")

def create_enhanced_project():
    """Create a new enhanced project with validation"""
    project_name = input("Please enter the new project name: ")

    # Category validation
    while True:
        try:
            category = input("Please enter the category: ")
            InvalidCategoryException.validate_category(category)
            break
        except InvalidCategoryException as e:
            print(e)

    # Year validation
    while True:
        try:
            year_started = input("Please enter the start year: ")
            InvalidYearException.validate_year(year_started)
            break
        except InvalidYearException as e:
            print(e)

    # State validation using regex
    while True:
        try:
            state_address = input("Please enter the full address (including state): ")
            InvalidStateAddressException.validate_state_address(state_address)
            # Extract city and state
            for state in InvalidStateAddressException.valid_states:
                if state in state_address:
                    city = state_address.replace(f", {state}", "").strip()
                    location = Location(state, city)
                    break
            break
        except InvalidStateAddressException as e:
            print(e)

    # Status validation
    while True:
        try:
            status = input("Please enter the project status (Current or Past): ")
            InvalidStatusException.validate_status(status)
            break
        except InvalidStatusException as e:
            print(e)

    # Budget validation using regex
    budget = ""
    while True:
        budget_input = input("Please enter the budget (e.g., $4.81m, $500k) or leave blank: ")
        if budget_input:
            try:
                InvalidBudgetException.validate_budget(budget_input)
                budget = budget_input
                break
            except InvalidBudgetException as e:
                print(e)
        else:
            break

    # Project period validation using regex
    project_period = ""
    while True:
        period_input = input("Please enter project period (DD/MM/YYYY – DD/MM/YYYY) or leave blank: ")
        if period_input:
            try:
                InvalidDateException.validate_date_range(period_input)
                project_period = period_input
                break
            except InvalidDateException as e:
                print(e)
        else:
            break

    # Create appropriate project type
    if status == "Current":
        project = EnhancedCurrentProject(project_name, category, year_started, location, budget, project_period)
    else:
        project = EnhancedPastProject(project_name, category, year_started, location, budget, project_period)

    # Set costs and funding with validation
    while True:
        cost = input("Do you know the total cost of this project (leave blank if you don't know): ")
        if cost:
            try:
                cost_value = float(cost)
                project.set_total_cost(cost_value)
                break
            except ValueError:
                print("Invalid input. Please enter a valid number for the cost.")
        else:
            break

    while True:
        funding = input("Do you know the total funding of this project (leave blank if you don't know): ")
        if funding:
            try:
                funding_value = float(funding)
                project.set_funding(funding_value)
                break
            except ValueError:
                print("Invalid input. Please enter a valid number for the funding.")
        else:
            break

    return project

def generate_summary_report(projects, search_type, search_value):
    """Generate textual summary report and visualizations"""
    if search_type == "category":
        filtered_projects = [p for p in projects if p.get_category() == search_value]
        filename_base = f"ARENA_report_{search_value.replace(' ', '_')}"
    else:  # state
        filtered_projects = [p for p in projects if search_value in p.get_location()]
        filename_base = f"ARENA_report_{search_value.replace(' ', '_')}"
    
    if not filtered_projects:
        print(f"No projects found for {search_type}: {search_value}")
        return
    
    # Generate text report
    try:
        with open(f"{filename_base}.txt", 'w') as file:
            file.write(f"ARENA Project Summary Report\n")
            file.write(f"Search Type: {search_type.title()}\n")
            file.write(f"Search Value: {search_value}\n")
            file.write(f"Total Projects Found: {len(filtered_projects)}\n")
            file.write("="*50 + "\n\n")
            
            for project in filtered_projects:
                file.write(str(project))
                if hasattr(project, 'get_budget') and project.get_budget():
                    file.write(f"    Budget: {project.get_budget()}\n")
                if hasattr(project, 'get_project_period') and project.get_project_period():
                    file.write(f"    Project Period: {project.get_project_period()}\n")
                file.write("\n")
        
        print(f"Text report saved as {filename_base}.txt")
    except IOError as e:
        print(f"Error writing report: {e}")
    
    # Generate visualizations
    visualizer = VisualizationDecorator(filtered_projects)
    title = f"{search_value} {search_type.title()} Analysis"
    
    visualizer.generate_bar_chart(title, filename_base)
    visualizer.generate_pie_chart(title, filename_base)
    visualizer.generate_line_chart(title, filename_base)

def main():
    """Main program with menu system"""
    manager = ProjectManager()
    
    # Try to load from JSON first, otherwise load from text file
    if not manager.load_from_json():
        manager.import_from_text()
    
    while True:
        print("\n" + "="*60)
        print("ARENA Project Management System - Enhanced Version")
        print("="*60)
        print("1. View all projects")
        print("2. Create new project")
        print("3. Search and modify projects")
        print("4. Generate summary report with visualizations")
        print("5. Import projects from text file")
        print("X/x. Exit program")
        print("="*60)
        
        try:
            choice = input("Please enter your choice: ").strip()
            InvalidChoiceException.validate_choice(choice)
        except InvalidChoiceException as e:
            print(e)
            continue
        
        if choice.upper() == 'X':
            # Save to both formats before exiting
            Project.write_project_to_file("ARENA_projects.txt")
            manager.save_to_json()
            print("Data saved successfully. Goodbye!")
            break
        
        elif choice == '1':
            Project.print_all_projects()
        
        elif choice == '2':
            project = create_enhanced_project()
            manager.projects.append(project)
            Project.projects = manager.projects
            print("Project created successfully!")
        
        elif choice == '3':
            name = input("Please enter the project name you want to search/edit: ")
            edit_project = Project.search_by_name(name)
            
            if edit_project is None:
                print("Project not found.")
                continue
            
            print("\nProject found:")
            print(edit_project)
            
            edit_choice = input("Do you want to edit this project? (y/n): ").lower()
            if edit_choice == 'y':
                attr_choice = input("Which attribute to edit? (1: category, 2: year, 3: budget, 4: period): ")
                
                if attr_choice == "1":
                    while True:
                        try:
                            new_category = input("Please enter the new category: ")
                            InvalidCategoryException.validate_category(new_category)
                            edit_project.set_category(new_category)
                            print("Category updated successfully!")
                            break
                        except InvalidCategoryException as e:
                            print(e)
                
                elif attr_choice == "2":
                    while True:
                        try:
                            new_year = input("Please enter the new start year: ")
                            InvalidYearException.validate_year(new_year)
                            edit_project.set_year_started(new_year)
                            print("Year updated successfully!")
                            break
                        except InvalidYearException as e:
                            print(e)
                
                elif attr_choice == "3" and hasattr(edit_project, 'set_budget'):
                    while True:
                        budget_input = input("Please enter the new budget (e.g., $4.81m): ")
                        try:
                            edit_project.set_budget(budget_input)
                            print("Budget updated successfully!")
                            break
                        except InvalidBudgetException as e:
                            print(e)
                
                elif attr_choice == "4" and hasattr(edit_project, 'set_project_period'):
                    while True:
                        period_input = input("Please enter the new project period (DD/MM/YYYY – DD/MM/YYYY): ")
                        try:
                            edit_project.set_project_period(period_input)
                            print("Project period updated successfully!")
                            break
                        except InvalidDateException as e:
                            print(e)
        
        elif choice == '4':
            search_type = input("Generate report by (1) category or (2) state: ")
            
            if search_type in ['1', 'category']:
                category = input("Please enter the category: ")
                generate_summary_report(manager.projects, "category", category)
            
            elif search_type in ['2', 'state']:
                state = input("Please enter the state name: ")
                generate_summary_report(manager.projects, "state", state)
            
            else:
                print("Invalid choice. Please enter 1, 2, 'category', or 'state'.")
        
        elif choice == '5':
            filename = input("Please enter the text file name (default: ARENA_projects.txt): ").strip()
            if not filename:
                filename = "ARENA_projects.txt"
            manager.import_from_text(filename)

if __name__ == "__main__":
    main()