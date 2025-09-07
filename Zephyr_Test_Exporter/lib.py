import csv
from datetime import datetime
import requests
import re

def get_cycles(project_version_map, BASE_URL, CYCLE_API_URL, CYCLE_FOLDERS_API_URL, AUTH):
    try:
        all_cycles = []

        for project_id, allowed_version_ids in project_version_map.items():
            response = requests.get(f"{BASE_URL}{CYCLE_API_URL}?projectId={project_id}", auth=AUTH)
            response.raise_for_status()
            response_data = response.json()

            for version_id, cycles_data in response_data.items():
                # Filter versions not in the allowed list
                if version_id not in allowed_version_ids:
                    continue

                for cycle in cycles_data:
                    for cycle_id, details in cycle.items():
                        if cycle_id in ("recordsCount", "-1"):
                            continue
                        folders = get_folders_for_cycle(project_id, cycle_id, version_id, BASE_URL, CYCLE_FOLDERS_API_URL, AUTH)
                        all_cycles.append({
                            "projectId": project_id,
                            "versionId": version_id,
                            "versionName": details['versionName'],
                            "cycleId": cycle_id,
                            "cycleName": details['name'],
                            "folders": folders
                        })
        return all_cycles

    except requests.exceptions.RequestException as e:
        print(f"Error fetching cycles: {e}")
        return []


def get_folders_for_cycle(project_id, cycle_id, version_id, BASE_URL, CYCLE_FOLDERS_API_URL, AUTH):
    try:
        response = requests.get(
            f"{BASE_URL}{CYCLE_FOLDERS_API_URL}?projectId={project_id}&versionId={version_id}".format(cycleId=cycle_id),
            auth=AUTH
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching folders for cycle {cycle_id}: {e}")
        return []

def get_folder_name(s: str) -> str:
    pattern = re.compile(r"\s*-?\s*(android|ios|chrome|firefox)$", re.IGNORECASE)
    return pattern.sub("", s).strip()

def get_platform(s: str) -> str | None:
    pattern = re.compile(r"(android|ios|chrome|firefox)$", re.IGNORECASE)
    match = pattern.search(s)
    if match:
        return match.group(1).lower()
    return None

def get_updated_time():
    current_time = datetime.now()
    return current_time.strftime("%d-%b %I:%M %p")

# Fetch and export cycles to CSV
def main(csv_filename: str, project_version_map, BASE_URL, CYCLE_API_URL, CYCLE_FOLDERS_API_URL, AUTH):
    updated_time = get_updated_time()
    cycles = get_cycles(project_version_map, BASE_URL, CYCLE_API_URL, CYCLE_FOLDERS_API_URL, AUTH)

    with open(csv_filename, mode="w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)

        # Write header
        csv_writer.writerow([
            "Date Updated", "Project", "Version", "Cycle", "Feature", "Platform", "Total TC", "EXECUTED",
            "UNEXECUTED", "PASSED", "FAILED", "BLOCKED", "WIP", "NA", "PENDING_RETEST"
        ])

        if cycles:
            for cycle in cycles:
                for folder in cycle["folders"]:

                    totalExecutions = folder['totalExecutions'] if folder['totalExecutions'] != 0 else 1
                    UNEXECUTED = ""
                    PASSED = ""
                    FAILED = ""
                    BLOCKED = ""
                    WIP = ""
                    NA = ""
                    PENDING_RETEST = ""

                    for executionSummary in folder["executionSummaries"]["executionSummary"]:
                        if executionSummary['statusName'] == "UNEXECUTED":
                            UNEXECUTED = executionSummary['count']
                        elif executionSummary['statusName'] == "PASSED":
                            PASSED = executionSummary['count']
                        elif executionSummary['statusName'] == "FAILED":
                            FAILED = executionSummary['count']
                        elif executionSummary['statusName'] == "BLOCKED":
                            BLOCKED = executionSummary['count']
                        elif executionSummary['statusName'] == "WIP":
                            WIP = executionSummary['count']
                        elif executionSummary['statusName'] == "NA":
                            NA = executionSummary['count']
                        elif executionSummary['statusName'] == "PENDING RETEST":
                            PENDING_RETEST = executionSummary['count']

                    # Write data to CSV
                    csv_writer.writerow([
                        updated_time, folder['projectName'], cycle['versionName'], cycle['cycleName'],
                        get_folder_name(folder['folderName']),get_platform(folder['folderName']),
                        totalExecutions, folder['totalExecuted'],
                        UNEXECUTED, PASSED, FAILED, BLOCKED, WIP, NA, PENDING_RETEST
                    ])
        else:
            print("No cycles found or an error occurred.")

    print(f"Results exported to {csv_filename}")


