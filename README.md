# ARENA Project Visualizer

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![matplotlib](https://img.shields.io/badge/matplotlib-charts-11557C)
![Tests](https://img.shields.io/badge/unittest-34%20passing-brightgreen)

A command-line tool for managing renewable-energy projects in the style of the Australian Renewable Energy Agency (ARENA)
portfolio. You can browse, create, search and edit projects, generate summary reports by category or state, and export
bar, line and pie charts. Data persists to JSON between sessions.

It's an object-oriented design exercise, so the focus is on the class model, validation and tests rather than on scale.

> Individual assignment for **CSIT121 Object-Oriented Design and Programming**, University of Wollongong (Autumn 2025).

## What I built

The assignment started from the teaching team's reference solution to the previous assignment: the base `Project` and
`Location` classes, the basic input validators and the menu skeleton. On top of that I built:

- **Multiple inheritance:** an `EnhancedProject` mix-in combined with `CurrentProject` / `PastProject` into
  `EnhancedCurrentProject` and `EnhancedPastProject`, adding budgets, project periods and funding data.
- **Design patterns:** `ProjectManager` is a singleton (via `__new__`) that owns persistence, and `VisualizationDecorator`
  adds bar, line and pie charts to a collection of projects without changing the model classes.
- **Stricter validation through custom exceptions:** regular expressions for budgets like `$4.81m` / `$500k`, date ranges like
  `01/12/2024 – 31/03/2028` (with real calendar checks and start-before-end), and state names inside free-text addresses.
- **Persistence and reporting:** JSON save and load, import from a legacy text format, and summary reports by category or state.
- **34 unit tests** with `unittest` and `unittest.mock`, covering the model, every validator, file I/O through temporary
  files, report generation and chart output.

## Run it

```bash
pip install matplotlib
python A3.py
```

The menu offers: view all projects, create a project, search and modify, generate a summary report with charts, and
import from a text file. `ARENA_projects.JSON` holds 16 sample projects.

**Run the tests.** In bash:

```bash
cd "Unit Test"
PYTHONPATH=.. python -m unittest test_A3 -v
```

In PowerShell:

```powershell
cd "Unit Test"
$env:PYTHONPATH = ".."; python -m unittest test_A3 -v
```

## Layout

```text
A3.py                  the complete application in one file (entry point)
models.py, manager.py, reporting.py, visualization.py, exceptions.py, cli.py
                       the same design split into modules
ARENA_projects.JSON    sample data
Unit Test/test_A3.py   34 unit tests
```

## Acknowledgements

The base classes, the basic validators and the menu skeleton come from the CSIT121 teaching team's reference solution to
the previous assignment, which was provided as the starting point. Everything listed under *What I built* is my own work.
