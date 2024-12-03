import requests
from tabulate import tabulate

# API Endpoint
GET_POLICIES_API = "http://localhost:8080/api/v1/policy"

# Authentication Token
API_KEY = "odt_xxxxxxxxxxxx"  # Replace with your actual token
HEADERS = {"X-Api-Key": API_KEY, "Content-Type": "application/json"}

def fetch_policies():
    """Fetch all policies."""
    response = requests.get(GET_POLICIES_API, headers=HEADERS)
    if response.status_code != 200:
        print(f"Error fetching policies: {response.status_code} - {response.text}")
        response.raise_for_status()
    return response.json()  # Expecting a list of policies

def process_policies(policies):
    """Extract relevant columns and arrange them alphabetically."""
    data = []
    for policy in policies:
        # Extract policy details
        policy_name = policy.get("name", "N/A")
        policy_uuid = policy.get("uuid", "N/A")

        # Extract project UUIDs linked to the policy
        project_uuids = ", ".join([project.get("uuid", "N/A") for project in policy.get("projects", [])])

        # Add extracted data to the list
        data.append([policy_name, policy_uuid, project_uuids])

    # Sort data alphabetically by policy name
    sorted_data = sorted(data, key=lambda x: x[0])  # Sort by the first column (Policy Name)
    return sorted_data

def display_policies(policies):
    """Display policies as a table using tabulate."""
    headers = ["Policy Name", "Policy UUID", "Applies to Project UUID"]
    table = tabulate(policies, headers=headers, tablefmt="plain")  # Use "plain" for simple format
    print(table)

def main():
    print("Fetching policies...")
    try:
        policies = fetch_policies()
        processed_policies = process_policies(policies)
        display_policies(processed_policies)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
