import json
import os

DATA_FILE = "database/data.json"

def load_data():
    """
    Load data from the JSON file and ensure all required keys exist.
    """
    if not os.path.exists(DATA_FILE):
        # Initialize with default data including the 'goals' key
        default_data = {
            "income": [],
            "expenses": [],
            "categories": [],
            "budget": {},
            "goals": []  # Ensuring 'goals' key exists
        }
        save_data(default_data)
        return default_data
    
    with open(DATA_FILE, "r") as file:
        data = json.load(file)

    # Ensure all required keys exist
    required_keys = ["income", "expenses", "categories", "budget", "goals"]
    for key in required_keys:
        if key not in data:
            data[key] = [] if key != "budget" else {}  # Initialize missing keys

    # Save the updated structure to ensure consistency
    save_data(data)

    return data

def save_data(data):
    """
    Save data to the JSON file while ensuring all required keys are present.
    """
    required_keys = ["income", "expenses", "categories", "budget", "goals"]
    for key in required_keys:
        if key not in data:
            data[key] = [] if key != "budget" else {}  # Initialize missing keys

    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)