import requests
from tabulate import tabulate  # For nice table formatting

# API Base URL
BASE_URL = "http://localhost:8080/api/v1"

# Authentication Token
API_KEY = "xxxxxxxx"  # Replace with your actual token
HEADERS = {"X-Api-Key": API_KEY}

def fetch_projects(tag=None):
    """Fetch all projects or projects filtered by a tag."""
    if tag:
        url = f"{BASE_URL}/project/tag/{tag}"
    else:
        url = f"{BASE_URL}/project"

    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def main():
    # Prompt the user for a tag
    tag = input("Enter a tag to filter projects (leave blank to fetch all projects): ").strip()

    # Fetch projects
    print(f"Fetching projects{' with tag ' + tag if tag else ''}...")
    projects = fetch_projects(tag if tag else None)

    # Prepare data for display
    display_data = [[project.get("name", "N/A"), project.get("uuid", "N/A")] for project in projects]

    # Print to screen in table format
    print("\n")
    print(tabulate(display_data, headers=["Project Name", "Project UUID"], tablefmt="plain"))

if __name__ == "__main__":
    main()
