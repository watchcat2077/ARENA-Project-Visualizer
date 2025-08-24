import matplotlib
matplotlib.use('Agg')  # ensure tests run without GUI
import matplotlib.pyplot as plt


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
            # Prefer internal accessor when available
            funding = getattr(project, '_get_funding_value', lambda: 0)()
            total_funding[cat] = total_funding.get(cat, 0) + (funding or 0)

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
            year = getattr(project, '_get_year_started_value', lambda: None)()
            if year is not None:
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
