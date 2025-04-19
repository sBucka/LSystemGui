import json
import os
from datetime import datetime
from . import utils

def load_systems_from_folder(folder_path: str) -> dict:
    """
    Load L-system data from JSON files in a specified folder.
    
    :param folder_path: Path to the folder containing JSON files.
    :return: Dictionary containing L-system data.
    """
    # If the folder_path is already a full path, use it directly
    if os.path.isabs(folder_path) and os.path.exists(folder_path):
        pass  # Use the path as is
    # Otherwise determine which directory to use based on the folder name
    elif isinstance(folder_path, str) and "examples" in folder_path:
        folder_path = utils.get_examples_dir()
    elif isinstance(folder_path, str) and "custom" in folder_path:
        folder_path = utils.get_custom_dir()
    else:
        # Default fallback - using relative path from base dir
        folder_path = os.path.join(utils.get_base_abs_path(), folder_path)
    
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    # Debug print
    print(f"Loading systems from: {folder_path}")
        
    systems = {}
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r') as file:
                system_name = os.path.splitext(filename)[0]
                systems[system_name] = json.load(file)
    if not systems:
        return None
    return systems

def export_systems_to_json(systems: dict) -> None:
    """
    Export L-system data to a JSON file.
    
    :param systems: Dictionary containing L-system data.
    :param file_path: Path to the JSON file.
    """
    # Use utils to get the custom directory path
    file_path = utils.get_custom_dir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"custom_{timestamp}.json"
    file_path = os.path.join(file_path, file_name)
    with open(file_path, 'w') as file:
        json.dump(systems, file, indent=4)
    return file_path