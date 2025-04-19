import os
import sys

def get_project_root():
    """
    Get the root directory of the project.
    """
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    if project_root not in sys.path:
        sys.path.append(project_root)
    return project_root

def get_animations_dir():
    """
    Get the path to the animations directory.
    """
    
    project_root = get_project_root()
    animations_dir = os.path.join(project_root, "animations")
    
    if not os.path.exists(animations_dir):
        os.makedirs(animations_dir)
    
    return animations_dir

def get_custom_dir():
    """
    Get the path to the custom directory.
    """
    
    project_root = get_project_root()
    custom_dir = os.path.join(project_root, "data", "custom")
    
    if not os.path.exists(custom_dir):
        os.makedirs(custom_dir)
    
    return custom_dir

def get_examples_dir():
    """
    Get the path to the examples directory.
    """
    
    project_root = get_project_root()
    examples_dir = os.path.join(project_root, "data", "examples")
    
    if not os.path.exists(examples_dir):
        os.makedirs(examples_dir)
    
    return examples_dir

def get_base_abs_path():
    """
    Get the absolute path to the base directory.
    """
    
    return os.path.dirname(os.path.abspath(__file__))
