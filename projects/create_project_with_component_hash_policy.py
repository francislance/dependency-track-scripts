import requests

# API Endpoints
BASE_URL = "http://localhost:8080/api/v1"
CREATE_PROJECT_API = f"{BASE_URL}/project"
CREATE_COMPONENT_API = f"{BASE_URL}/component/project"
CREATE_POLICY_API = f"{BASE_URL}/policy"
ADD_POLICY_CONDITION_API = f"{BASE_URL}/policy"  # Append /{uuid}/condition dynamically
ADD_PROJECT_TO_POLICY_API = f"{BASE_URL}/policy"  # Append /{policyUuid}/project/{projectUuid} dynamically

# Authentication Token
API_KEY = "odt_xyxyxyxyyxyxyxyyxyx"  # Replace with your actual token
HEADERS = {"X-Api-Key": API_KEY, "Content-Type": "application/json"}

def create_project(project_name):
    """Create a project with the given name."""
    project_name_with_instances = f"{project_name} [Instances]"
    payload = {"name": project_name_with_instances}
    response = requests.put(CREATE_PROJECT_API, json=payload, headers=HEADERS)
    if response.status_code != 201:
        print(f"Error creating project: {response.status_code} - {response.text}")
        response.raise_for_status()
    return response.json()  # Expecting the created project details with UUID

def create_component(project_uuid, component_name, sha256_hash):
    """Create a component under a project with a specific SHA256 hash."""
    payload = {
        "name": component_name,
        "sha256": sha256_hash
    }
    response = requests.put(f"{CREATE_COMPONENT_API}/{project_uuid}", json=payload, headers=HEADERS)
    if response.status_code != 201:
        print(f"Error creating component: {response.status_code} - {response.text}")
        response.raise_for_status()
    return response.json()  # Expecting the created component details

def create_policy(policy_name, project_uuid):
    """Create a policy with specified projects."""
    payload = {
        "name": policy_name,
        "operator": "ALL",
        "violationState": "FAIL",
        "projects": [
            {"uuid": project_uuid}
        ],
        "global": True
    }

    response = requests.put(CREATE_POLICY_API, json=payload, headers=HEADERS)
    if response.status_code != 201:
        print(f"Error creating policy: {response.status_code} - {response.text}")
        response.raise_for_status()
    return response.json()  # Expecting the created policy details with UUID

def add_policy_condition(policy_uuid, operator, subject, value):
    """Add a condition to an existing policy."""
    payload = {
        "operator": operator,
        "subject": subject,
        "value": value
    }
    url = f"{ADD_POLICY_CONDITION_API}/{policy_uuid}/condition"
    response = requests.put(url, json=payload, headers=HEADERS)
    if response.status_code != 201:
        print(f"Error adding condition: {response.status_code} - {response.text}")
        response.raise_for_status()
    return response.json()  # Expecting the updated policy details

def add_project_to_policy(policy_uuid, project_uuid):
    """Add a project to an existing policy."""
    url = f"{ADD_PROJECT_TO_POLICY_API}/{policy_uuid}/project/{project_uuid}"
    response = requests.post(url, headers=HEADERS)
    if response.status_code != 200:
        print(f"Error adding project to policy: {response.status_code} - {response.text}")
        response.raise_for_status()
    return response.json()  # Expecting confirmation of the added project

def main():
    # Input values
    project_name = input("Enter the project name: ")
    X = int(input("Enter the number of components to create: "))
    component_name = input("Enter the base name for components: ")
    sha256_hash = input("Enter the SHA256 hash value to use for all components: ")

    # Step 1: Create the project
    print("Creating project...")
    try:
        project = create_project(project_name)
        project_uuid = project["uuid"]
        print(f"Project created with UUID: {project_uuid}")
    except Exception as e:
        print(f"Failed to create project: {e}")
        return

    # Step 2: Create components in a loop
    print("Creating components...")
    for i in range(1, X + 1):
        try:
            component_full_name = f"{component_name} [Instance {i}]"
            create_component(project_uuid, component_full_name, sha256_hash)
            print(f"Created component: {component_full_name}")
        except Exception as e:
            print(f"Failed to create component {component_full_name}: {e}")
            continue  # Skip to the next component

    # Step 3: Create policy
    print("Creating policy...")
    try:
        policy_name = f"[Component Hash] {project_name}"
        policy = create_policy(policy_name, project_uuid)
        policy_uuid = policy["uuid"]
        print(f"Policy created with UUID: {policy_uuid}")
    except Exception as e:
        print(f"Failed to create policy: {e}")
        return

    # Step 4: Add policy condition
    print("Adding policy condition...")
    try:
        condition_operator = "IS_NOT"
        condition_subject = "COMPONENT_HASH"
        condition_value = f'{{"algorithm":"SHA-256","value":"{sha256_hash}"}}'
        add_policy_condition(policy_uuid, condition_operator, condition_subject, condition_value)
        print("Policy condition added successfully.")
    except Exception as e:
        print(f"Failed to add policy condition: {e}")
        return

    # Step 5: Add project to policy
    print("Adding project to policy...")
    try:
        add_project_to_policy(policy_uuid, project_uuid)
        print("Project added to policy successfully.")
    except Exception as e:
        print(f"Failed to add project to policy: {e}")
        return

    print("All tasks completed successfully.")

if __name__ == "__main__":
    main()
