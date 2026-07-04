import sys
import json
from pathlib import Path

import yaml
PROJECT_ROOT = Path(__file__).resolve().parents[3]

def load_platform_schema(schema_path: str):
    """
    Load the schema for a given entity from the platform schemas directory.

    Args:
        schema_name (str): Name of the schema file (without .json extension).
    Returns:
        dict: The loaded schema as a dictionary.
    """
    #schema_path = PROJECT_ROOT / "configs" / "framework" / f"{schema_name}_schema.yaml"
    if not schema_path.exists():
        raise FileNotFoundError(f"Schema file not found: {schema_path}")
    
    
    with open(schema_path, 'r') as file:
        schema = yaml.safe_load(file)
    
    return schema