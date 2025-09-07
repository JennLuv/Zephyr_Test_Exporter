from config import AUTH
from lib import main

# Replace with your API endpoint and credentials
BASE_URL = "https://your_base_url/rest/zapi"
CYCLE_API_URL = "/latest/cycle"
CYCLE_FOLDERS_API_URL = "/latest/cycle/{cycleId}/folders"

# #### Tvt
project_version_map = {
    "00000": ["00000","00000","00000"],
    "00000": ["00000","00000","00000"]
}

# Replace with your desired csv name
csv_filename = "../Zephyr_Test_Exporter/Test_output.csv"

if __name__ == "__main__" :
    main(csv_filename, project_version_map, BASE_URL, CYCLE_API_URL, CYCLE_FOLDERS_API_URL, AUTH)



