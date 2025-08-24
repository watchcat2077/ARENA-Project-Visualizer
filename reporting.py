from .visualization import VisualizationDecorator


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
