import requests
import csv
from tabulate import tabulate  # For nice table formatting

# API Base URL
BASE_URL = "http://localhost:8080/api/v1"

# Authentication Token
API_KEY = "odt_xyxyxyxyxyxyY"  # Replace with your actual token
HEADERS = {"X-Api-Key": API_KEY}

# Output CSV file
OUTPUT_CSV_FILE = "project_components.csv"

def fetch_project_tags(tag):
    """Fetch projects with the specified tag."""
    tag_api = f"{BASE_URL}/project/tag/{tag}"
    response = requests.get(tag_api, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def fetch_project_components(project_uuid):
    """Fetch components for a given project UUID."""
    response = requests.get(f"{BASE_URL}/component/project/{project_uuid}", headers=HEADERS)
    response.raise_for_status()
    return response.json()

def main():
    # Prompt the user for the tag
    tag = input("Enter the tag to filter projects (e.g., springboot): ").strip()

    # Fetch project tags based on the input tag
    print(f"Fetching projects with the tag '{tag}'...")
    projects = fetch_project_tags(tag)

    # Prepare data for CSV and display
    csv_data = []
    display_data = []

    for project in projects:
        project_name = project.get("name")
        project_uuid = project.get("uuid")

        # Fetch components for the project
        components = fetch_project_components(project_uuid)

        for component in components:
            component_name = component.get("name")
            sha256 = component.get("sha256")

            # Append to CSV data
            csv_data.append({
                "Project Name": project_name,
                "Component Name": component_name,
                "Sha256": sha256
            })

            # Append to display data
            display_data.append([project_name, component_name, sha256])

    # Write to CSV
    with open(OUTPUT_CSV_FILE, mode="w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["Project Name", "Component Name", "Sha256"])
        writer.writeheader()
        writer.writerows(csv_data)

    # Print to screen in table format
    print("\n")
    print(tabulate(display_data, headers=["Project Name", "Component Name", "Sha256"], tablefmt="plain"))
    print(f"\nResults have been written to '{OUTPUT_CSV_FILE}'.")

if __name__ == "__main__":
    main()
