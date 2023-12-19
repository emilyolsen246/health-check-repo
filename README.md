# Health Check

## Description

This program continuously monitors the health of specified endpoints from a YML file, calculates availability percentages for each domain, and logs the results. It repeats this process every 15 seconds until the user interrupts the program.

## Instructions

1. Clone this repo: `git clone https://github.com/emilyolsen246/health-check-repo.git`
2. Upload any YML test file in the appropriate format to /input
3. Create the virtual environment: `python3 -m venv .venv`
4. Activate it: `source .venv/bin/activate`
5. Install dependencies: `pip install -r requirements.txt`
6. Run the program: `python3 health-check-solution.py`
7. The program will prompt you for a path to the YML file.
8. The results of the program will be logged to the console until you exit (Ctrl+C).