from .exceptions import (
    InvalidChoiceException,
    InvalidCategoryException,
    InvalidYearException,
    InvalidStateAddressException,
    InvalidStatusException,
    InvalidBudgetException,
    InvalidDateException,
)
from .manager import ProjectManager
from .models import Location, EnhancedCurrentProject, EnhancedPastProject, Project
from .reporting import generate_summary_report


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


def main():
    """Main program with menu system"""
    manager = ProjectManager()

    # Try to load from JSON first, otherwise load from text file
    if not manager.load_from_json():
        manager.import_from_text()

    while True:
        print("\n" + "=" * 60)
        print("ARENA Project Management System - Enhanced Version")
        print("=" * 60)
        print("1. View all projects")
        print("2. Create new project")
        print("3. Search and modify projects")
        print("4. Generate summary report with visualizations")
        print("5. Import projects from text file")
        print("X/x. Exit program")
        print("=" * 60)

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
