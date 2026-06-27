import yaml
import os
from pathlib import Path
def load_config(env):
    """
    Load configuration from a YAML file.

    Args:
        file_path (str): Path to the YAML configuration file.
        env (str): Environment name to load specific configuration (default: "local").

    """
    project_root = Path(__file__).resolve().parents[2]

    file_path = project_root / "configs" / "env" / f"{env}.yaml"

    if not file_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {file_path}")

    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
        return config
    
    