import re
from datetime import datetime


class InvalidChoiceException(Exception):
    @staticmethod
    def validate_choice(choice):
        if choice not in ['1', '2', '3', '4', '5', 'x', 'X']:
            raise InvalidChoiceException(f"Invalid choice: {choice}")


class InvalidCategoryException(Exception):
    valid_category = [
        "Bioenergy",
        "Energy from waste",
        "Battery storage",
        "Solar energy",
        "Distributed energy resources",
        "Electric vehicles",
        "Wind energy",
        "Education",
    ]

    @staticmethod
    def validate_category(category):
        if category not in InvalidCategoryException.valid_category:
            raise InvalidCategoryException(f"Invalid category: {category}")


class InvalidStateException(Exception):
    valid_state = [
        "Australian Capital Territory",
        "National",
        "New South Wales",
        "Northern Territory",
        "Queensland",
        "South Australia",
        "Tasmania",
        "Victoria",
        "Western Australia",
    ]

    @staticmethod
    def validate_state(state):
        if state not in InvalidStateException.valid_state:
            raise InvalidStateException(f"Invalid state: {state}")


class InvalidCityException(Exception):
    valid_city = [
        "Sydney",
        "Melbourne",
        "Brisbane",
        "Perth",
        "Adelaide",
        "Canberra",
        "Hobart",
        "Darwin",
        "Gold Coast",
        "Newcastle",
        "Wollongong",
        "Geelong",
        "Townsville",
        "Cairns",
        "Toowoomba",
        "Ballarat",
        "Bendigo",
        "Launceston",
        "Mackay",
        "Rockhampton",
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
            raise InvalidBudgetException(
                f"Invalid budget format: {budget_str}. Use format like $4.81m or $500k"
            )


class InvalidDateException(Exception):
    @staticmethod
    def validate_date_range(date_range):
        # Pattern for date range: DD/MM/YYYY – DD/MM/YYYY (requires spaces around dash)
        pattern = r'^\d{2}/\d{2}/\d{4}\s+[\u2013-]\s+\d{2}/\d{2}/\d{4}$'
        if not re.match(pattern, date_range):
            raise InvalidDateException(
                f"Invalid date format: {date_range}. Use format: DD/MM/YYYY – DD/MM/YYYY"
            )

        # Validate actual dates - handle both dash types
        try:
            # Split on either type of dash
            if '\u2013' in date_range:
                dates = date_range.split('\u2013')
            else:
                dates = date_range.split('-')

            start_date_str = dates[0].strip()
            end_date_str = dates[1].strip()

            # Validate date format more strictly
            if not re.match(r'^\d{2}/\d{2}/\d{4}$', start_date_str) or not re.match(
                r'^\d{2}/\d{2}/\d{4}$', end_date_str
            ):
                raise InvalidDateException(f"Invalid date format in: {date_range}")

            start_date = datetime.strptime(start_date_str, '%d/%m/%Y')
            end_date = datetime.strptime(end_date_str, '%d/%m/%Y')

            if start_date >= end_date:
                raise InvalidDateException("Start date must be before end date")

        except ValueError:
            raise InvalidDateException(f"Invalid date values in: {date_range}")


class InvalidStateAddressException(Exception):
    valid_states = [
        "Australian Capital Territory",
        "National",
        "New South Wales",
        "Northern Territory",
        "Queensland",
        "South Australia",
        "Tasmania",
        "Victoria",
        "Western Australia",
    ]

    @staticmethod
    def validate_state_address(address):
        # Check if any valid state is in the address
        for state in InvalidStateAddressException.valid_states:
            if state in address:
                return
        raise InvalidStateAddressException(f"Invalid state address: {address}")
