<img width="1000" height="239" alt="image" src="https://github.com/user-attachments/assets/4cabfabb-4a94-4c70-a286-f723275e6dc0" />

The Jira Zephyr Cycles Exporter is a Python utility that retrieves test cycle data from Zephyr for Jira and exports it into a structured CSV file.

It connects to the Jira Zephyr API, fetches cycle summaries, including execution counts and statuses, and formats them into a clean, tabular CSV. This makes it easy to analyze testing progress in tools like Excel or Google Sheets.

Follow these steps to configure and run the Jira Zephyr Cycles Exporter:
1. Install Requirements
This project requires Python 3.8+ and the requests library.
pip install requests

2. Configure Authentication
Open config.py and fill in your Jira username and password:
AUTH = ("your_username", "your_password")

3. Set Your Jira Base URL
In run.py, set the base URL of your Jira instance:
BASE_URL = "https://yourcompany.atlassian.net"

4. Get Project and Version IDs
- Open Jira in your browser.
- Navigate to the Zephyr test cycle you want to export.
- From the URL or network requests, find the projectId and versionId.
- Update run.py with those values in the project_version_map:
project_version_map = {
    "12345": ["67890"],  # Example: projectId: versionId
}

5. Run the Exporter
From the project root, run:
python run.py

6. View Results in Excel
The script will generate a CSV file (default: Test_output.csv) that you can open directly in Excel for analysis.
