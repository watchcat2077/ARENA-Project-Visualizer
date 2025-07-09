import unittest
import json
import os
import tempfile
from unittest.mock import patch, mock_open
from A3 import (
    Project, EnhancedProject, EnhancedCurrentProject, EnhancedPastProject, 
    ProjectManager, VisualizationDecorator, Location,
    InvalidBudgetException, InvalidDateException, InvalidStateAddressException,
    InvalidCategoryException, InvalidYearException, InvalidStatusException,
    InvalidChoiceException, create_enhanced_project, generate_summary_report
)

class TestProject(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        Project.projects = []  # Reset projects list
        self.location = Location("New South Wales", "Sydney")
        self.project = Project("Test Project", "Solar energy", "2020", self.location)
    
    def tearDown(self):
        """Clean up after each test method."""
        Project.projects = []
    
    def test_project_creation(self):
        """Test basic project creation"""
        self.assertEqual(self.project.get_name(), "Test Project")
        self.assertEqual(self.project.get_category(), "Solar energy")
        self.assertEqual(self.project.get_location(), "Sydney, New South Wales")
    
    def test_project_str_representation(self):
        """Test project string representation"""
        str_repr = str(self.project)
        self.assertIn("Test Project", str_repr)
        self.assertIn("Solar energy", str_repr)
        self.assertIn("2020", str_repr)
    
    def test_add_to_list(self):
        """Test adding project to projects list"""
        self.project.add_to_list()
        self.assertEqual(len(Project.projects), 1)
        self.assertEqual(Project.projects[0], self.project)
    
    def test_search_by_name(self):
        """Test searching project by name"""
        self.project.add_to_list()
        found_project = Project.search_by_name("Test Project")
        self.assertEqual(found_project, self.project)
        
        not_found = Project.search_by_name("Non-existent Project")
        self.assertIsNone(not_found)
    
    def test_set_and_get_funding(self):
        """Test setting and getting funding"""
        self.project.set_funding(100000)
        self.assertEqual(self.project.get_funding(), "Funding: 100000")
    
    def test_set_and_get_total_cost(self):
        """Test setting and getting total cost"""
        self.project.set_total_cost(500000)
        self.assertEqual(self.project.get_total_cost(), "Total Cost: 500000")

class TestLocation(unittest.TestCase):
    
    def test_location_creation(self):
        """Test location creation and string representation"""
        location = Location("Victoria", "Melbourne")
        self.assertEqual(str(location), "Melbourne, Victoria")
        self.assertEqual(location.get_state(), "Victoria")

class TestExceptionValidation(unittest.TestCase):
    
    def test_invalid_budget_exception(self):
        """Test budget validation"""
        # Valid budgets
        valid_budgets = ["$4.81m", "$500k", "$1.00m", "$999k"]
        for budget in valid_budgets:
            try:
                InvalidBudgetException.validate_budget(budget)
            except InvalidBudgetException:
                self.fail(f"Valid budget {budget} raised InvalidBudgetException")
        
        # Invalid budgets
        invalid_budgets = ["4.81m", "$4.8", "$4.81", "4.81", "$4.81x", ""]
        for budget in invalid_budgets:
            with self.assertRaises(InvalidBudgetException):
                InvalidBudgetException.validate_budget(budget)
    
    def test_invalid_date_exception(self):
        """Test date range validation"""
        # Valid dates
        valid_dates = ["01/12/2024 – 31/03/2028", "15/06/2020 – 30/11/2025", "01/01/2021 - 31/12/2025"]
        for date_range in valid_dates:
            try:
                InvalidDateException.validate_date_range(date_range)
            except InvalidDateException:
                self.fail(f"Valid date range {date_range} raised InvalidDateException")
        
        # Invalid dates
        invalid_dates = [
            "01/12/2024-31/03/2028",  # No spaces around dash
            "1/12/2024 – 31/03/2028",  # Wrong day format
            "01/12/24 – 31/03/28",     # Wrong year format
            "31/03/2028 – 01/12/2024", # End before start
            "32/12/2024 – 31/03/2028", # Invalid day
            "01/13/2024 – 31/03/2028"  # Invalid month
        ]
        for date_range in invalid_dates:
            with self.assertRaises(InvalidDateException):
                InvalidDateException.validate_date_range(date_range)
    
    def test_invalid_state_address_exception(self):
        """Test state address validation"""
        # Valid addresses
        valid_addresses = [
            "Sydney, New South Wales",
            "Melbourne, Victoria", 
            "Brisbane, Queensland",
            "Perth, Western Australia"
        ]
        for address in valid_addresses:
            try:
                InvalidStateAddressException.validate_state_address(address)
            except InvalidStateAddressException:
                self.fail(f"Valid address {address} raised InvalidStateAddressException")
        
        # Invalid addresses
        invalid_addresses = [
            "Sydney, NSW",
            "Melbourne, VIC",
            "Unknown City, Invalid State"
        ]
        for address in invalid_addresses:
            with self.assertRaises(InvalidStateAddressException):
                InvalidStateAddressException.validate_state_address(address)
    
    def test_invalid_category_exception(self):
        """Test category validation"""
        # Valid category
        InvalidCategoryException.validate_category("Solar energy")
        
        # Invalid category
        with self.assertRaises(InvalidCategoryException):
            InvalidCategoryException.validate_category("Invalid Category")
    
    def test_invalid_year_exception(self):
        """Test year validation"""
        # Valid year
        InvalidYearException.validate_year("2020")
        
        # Invalid year
        with self.assertRaises(InvalidYearException):
            InvalidYearException.validate_year("2030")
    
    def test_invalid_status_exception(self):
        """Test status validation"""
        # Valid statuses
        InvalidStatusException.validate_status("Current")
        InvalidStatusException.validate_status("Past")
        
        # Invalid status
        with self.assertRaises(InvalidStatusException):
            InvalidStatusException.validate_status("Unknown")
    
    def test_invalid_choice_exception(self):
        """Test choice validation"""
        # Valid choices
        valid_choices = ['1', '2', '3', '4', '5', 'x', 'X']
        for choice in valid_choices:
            InvalidChoiceException.validate_choice(choice)
        
        # Invalid choice
        with self.assertRaises(InvalidChoiceException):
            InvalidChoiceException.validate_choice("6")

class TestEnhancedProject(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.location = Location("Queensland", "Brisbane")
        self.project = EnhancedProject(
            "Enhanced Test", "Wind energy", "2021", self.location, 
            "$2.50m", "01/01/2021 – 31/12/2025"
        )
    
    def test_enhanced_project_creation(self):
        """Test enhanced project creation with budget and period"""
        self.assertEqual(self.project.get_name(), "Enhanced Test")
        self.assertEqual(self.project.get_budget(), "$2.50m")
        self.assertEqual(self.project.get_project_period(), "01/01/2021 – 31/12/2025")
    
    def test_budget_setter_validation(self):
        """Test budget setter with validation"""
        self.project.set_budget("$3.00m")
        self.assertEqual(self.project.get_budget(), "$3.00m")
        
        with self.assertRaises(InvalidBudgetException):
            self.project.set_budget("invalid_budget")
    
    def test_project_period_setter_validation(self):
        """Test project period setter with validation"""
        self.project.set_project_period("01/06/2022 – 30/05/2027")
        self.assertEqual(self.project.get_project_period(), "01/06/2022 – 30/05/2027")
        
        with self.assertRaises(InvalidDateException):
            self.project.set_project_period("invalid_date")
    
    def test_to_dict(self):
        """Test project to dictionary conversion"""
        project_dict = self.project.to_dict()
        
        expected_keys = ['name', 'category', 'year_started', 'location', 
                        'total_cost', 'funding', 'budget', 'project_period', 'type']
        
        for key in expected_keys:
            self.assertIn(key, project_dict)
        
        self.assertEqual(project_dict['name'], "Enhanced Test")
        self.assertEqual(project_dict['budget'], "$2.50m")
        self.assertEqual(project_dict['project_period'], "01/01/2021 – 31/12/2025")
    
    def test_from_dict(self):
        """Test project creation from dictionary"""
        project_dict = {
            'name': 'Dict Test',
            'category': 'Battery storage',
            'year_started': '2022',
            'location': 'Adelaide, South Australia',
            'total_cost': 800000,
            'funding': 600000,
            'budget': '$3.50m',
            'project_period': '01/06/2022 – 30/05/2027',
            'type': 'EnhancedProject'
        }
        
        project = EnhancedProject.from_dict(project_dict)
        
        self.assertEqual(project.get_name(), 'Dict Test')
        self.assertEqual(project.get_category(), 'Battery storage')
        self.assertEqual(project.get_budget(), '$3.50m')
        self.assertEqual(project.get_project_period(), '01/06/2022 – 30/05/2027')

class TestEnhancedCurrentProject(unittest.TestCase):
    
    def test_current_project_creation(self):
        """Test current project creation"""
        location = Location("Tasmania", "Hobart")
        project = EnhancedCurrentProject(
            "Current Test", "Bioenergy", "2023", location, "$1.50m", "01/01/2023 – 31/12/2028"
        )
        
        self.assertEqual(project.get_name(), "Current Test")
        self.assertEqual(project.get_budget(), "$1.50m")
        self.assertIsInstance(project, EnhancedCurrentProject)
    
    def test_current_project_serialization(self):
        """Test CurrentProject serialization/deserialization"""
        location = Location("Tasmania", "Hobart")
        current_project = EnhancedCurrentProject("Current Test", "Bioenergy", "2023", location)
        project_dict = current_project.to_dict()
        
        self.assertEqual(project_dict['type'], 'EnhancedCurrentProject')
        
        restored_project = EnhancedProject.from_dict(project_dict)
        self.assertIsInstance(restored_project, EnhancedCurrentProject)
        self.assertEqual(restored_project.get_name(), "Current Test")

class TestEnhancedPastProject(unittest.TestCase):
    
    def test_past_project_creation(self):
        """Test past project creation"""
        location = Location("Western Australia", "Perth")
        project = EnhancedPastProject(
            "Past Test", "Electric vehicles", "2019", location, "$800k", "01/01/2019 – 31/12/2022"
        )
        
        self.assertEqual(project.get_name(), "Past Test")
        self.assertEqual(project.get_budget(), "$800k")
        self.assertIsInstance(project, EnhancedPastProject)
    
    def test_past_project_serialization(self):
        """Test PastProject serialization/deserialization"""
        location = Location("Western Australia", "Perth")
        past_project = EnhancedPastProject("Past Test", "Electric vehicles", "2019", location)
        project_dict = past_project.to_dict()
        
        self.assertEqual(project_dict['type'], 'EnhancedPastProject')
        
        restored_project = EnhancedProject.from_dict(project_dict)
        self.assertIsInstance(restored_project, EnhancedPastProject)
        self.assertEqual(restored_project.get_name(), "Past Test")

class TestProjectManager(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        # Reset singleton instance for testing
        ProjectManager._instance = None
        self.manager = ProjectManager()
        self.temp_dir = tempfile.mkdtemp()
        self.json_file = os.path.join(self.temp_dir, "test_projects.json")
        
        # Create test project
        location = Location("Queensland", "Brisbane")
        self.test_project = EnhancedProject(
            "Manager Test", "Solar energy", "2020", location, "$2.00m", "01/01/2020 – 31/12/2025"
        )
        self.test_project.set_total_cost(500000)
        self.test_project.set_funding(300000)
        self.manager.projects = [self.test_project]
    
    def tearDown(self):
        """Clean up temp files"""
        if os.path.exists(self.json_file):
            os.remove(self.json_file)
        os.rmdir(self.temp_dir)
        # Reset singleton
        ProjectManager._instance = None
    
    def test_singleton_pattern(self):
        """Test that ProjectManager follows singleton pattern"""
        manager1 = ProjectManager()
        manager2 = ProjectManager()
        self.assertIs(manager1, manager2)
    
    def test_save_to_json(self):
        """Test saving projects to JSON file"""
        self.manager.save_to_json(self.json_file)
        
        self.assertTrue(os.path.exists(self.json_file))
        
        with open(self.json_file, 'r') as file:
            data = json.load(file)
        
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], "Manager Test")
        self.assertEqual(data[0]['budget'], "$2.00m")
    
    def test_load_from_json(self):
        """Test loading projects from JSON file"""
        # First save the project
        self.manager.save_to_json(self.json_file)
        
        # Clear projects and reload
        self.manager.projects = []
        result = self.manager.load_from_json(self.json_file)
        
        self.assertTrue(result)
        self.assertEqual(len(self.manager.projects), 1)
        
        loaded_project = self.manager.projects[0]
        self.assertEqual(loaded_project.get_name(), "Manager Test")
        self.assertEqual(loaded_project.get_budget(), "$2.00m")
    
    def test_load_from_nonexistent_json(self):
        """Test loading from non-existent JSON file"""
        result = self.manager.load_from_json("nonexistent.json")
        self.assertFalse(result)
    
    @patch('builtins.open', new_callable=mock_open, read_data='')
    def test_import_from_text_file_not_found(self, mock_file):
        """Test importing from non-existent text file"""
        mock_file.side_effect = FileNotFoundError()
        with patch('builtins.print') as mock_print:
            self.manager.import_from_text("nonexistent.txt")
            mock_print.assert_called()

class TestVisualizationDecorator(unittest.TestCase):
    
    def setUp(self):
        """Set up test projects for visualization"""
        location1 = Location("New South Wales", "Sydney")
        location2 = Location("Victoria", "Melbourne")
        
        self.projects = [
            EnhancedProject("Solar 1", "Solar energy", "2020", location1),
            EnhancedProject("Wind 1", "Wind energy", "2021", location2),
            EnhancedProject("Solar 2", "Solar energy", "2022", location1)
        ]
        
        # Set some funding for testing
        self.projects[0].set_funding(100000)
        self.projects[1].set_funding(200000)
        self.projects[2].set_funding(150000)
        
        self.visualizer = VisualizationDecorator(self.projects)
    
    @patch('matplotlib.pyplot.show')
    @patch('matplotlib.pyplot.savefig')
    def test_bar_chart_generation(self, mock_savefig, mock_show):
        """Test bar chart generation"""
        self.visualizer.generate_bar_chart("Test", "test_output")
        mock_savefig.assert_called_once_with('test_output_bar_chart.png')
        mock_show.assert_called_once()
    
    @patch('matplotlib.pyplot.show')
    @patch('matplotlib.pyplot.savefig')
    def test_pie_chart_generation(self, mock_savefig, mock_show):
        """Test pie chart generation"""
        self.visualizer.generate_pie_chart("Test", "test_output")
        mock_savefig.assert_called_once_with('test_output_pie_chart.png')
        mock_show.assert_called_once()
    
    @patch('matplotlib.pyplot.show')
    @patch('matplotlib.pyplot.savefig')
    def test_line_chart_generation(self, mock_savefig, mock_show):
        """Test line chart generation"""
        self.visualizer.generate_line_chart("Test", "test_output")
        mock_savefig.assert_called_once_with('test_output_line_chart.png')
        mock_show.assert_called_once()

class TestFunctionality(unittest.TestCase):
    
    def setUp(self):
        """Set up test projects"""
        Project.projects = []
        location1 = Location("Victoria", "Melbourne")
        location2 = Location("Queensland", "Brisbane")
        
        self.project1 = EnhancedProject("Func Test 1", "Solar energy", "2020", location1)
        self.project2 = EnhancedProject("Func Test 2", "Wind energy", "2021", location2)
        
        Project.projects = [self.project1, self.project2]
    
    def tearDown(self):
        """Clean up"""
        Project.projects = []
    
    @patch('builtins.input', side_effect=[
        "Test Project",  # project name
        "Solar energy",  # category
        "2020",  # year
        "Sydney, New South Wales",  # address
        "Current",  # status
        "$1.50m",  # budget
        "01/01/2020 – 31/12/2025",  # period
        "100000",  # cost
        "75000"  # funding
    ])
    def test_create_enhanced_project(self, mock_input):
        """Test creating an enhanced project with mocked input"""
        project = create_enhanced_project()
        
        self.assertEqual(project.get_name(), "Test Project")
        self.assertEqual(project.get_category(), "Solar energy")
        self.assertEqual(project.get_budget(), "$1.50m")
        self.assertEqual(project.get_project_period(), "01/01/2020 – 31/12/2025")
        self.assertIsInstance(project, EnhancedCurrentProject)
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('matplotlib.pyplot.show')
    @patch('matplotlib.pyplot.savefig')
    def test_generate_summary_report(self, mock_savefig, mock_show, mock_file):
        """Test generating summary report"""
        generate_summary_report([self.project1, self.project2], "category", "Solar energy")
        
        # Check that file was opened for writing
        mock_file.assert_called()
        
        # Check that visualizations were generated
        self.assertEqual(mock_savefig.call_count, 3)  # bar, pie, line charts
        self.assertEqual(mock_show.call_count, 3)

class TestFileOperations(unittest.TestCase):
    
    def setUp(self):
        """Set up for file operation tests"""
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.temp_dir, "test_projects.txt")
        Project.projects = []
    
    def tearDown(self):
        """Clean up temp files"""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        os.rmdir(self.temp_dir)
        Project.projects = []
    
    def test_write_project_to_file(self):
        """Test writing projects to file"""
        location = Location("Victoria", "Melbourne")
        project = Project("File Test", "Solar energy", "2020", location)
        project.add_to_list()
        
        Project.write_project_to_file(self.test_file)
        
        self.assertTrue(os.path.exists(self.test_file))
        
        with open(self.test_file, 'r') as file:
            content = file.read()
            self.assertIn("File Test", content)
            self.assertIn("Solar energy", content)

if __name__ == '__main__':
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestProject, TestLocation, TestExceptionValidation,
        TestEnhancedProject, TestEnhancedCurrentProject, TestEnhancedPastProject,
        TestProjectManager, TestVisualizationDecorator, TestFunctionality,
        TestFileOperations
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print test summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\nFAILURES:")
        for test, traceback in result.failures:
            print(f"- {test}")
    
    if result.errors:
        print("\nERRORS:")
        for test, traceback in result.errors:
            print(f"- {test}")
    
    success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100) if result.testsRun > 0 else 0
    print(f"Success rate: {success_rate:.1f}%")