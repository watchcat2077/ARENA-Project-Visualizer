import json

from .models import Project, EnhancedProject


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
                project._get_year_started_value(),
                project._get_location_obj(),
            )
            enhanced_project.set_total_cost(project._get_total_cost_value())
            enhanced_project.set_funding(project._get_funding_value())
            enhanced_projects.append(enhanced_project)

        self.projects = enhanced_projects
        Project.projects = self.projects
