from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from common.config_loader import load_config
import yaml
from pathlib import Path


def load_entity_config(entity_name):
    """
    Load entity-specific configuration from a YAML file.

    Args:
        entity_name (str): Name of the entity to load configuration for.
        env (str): Environment name to load specific configuration (default: "local").

    Returns:
        dict: Configuration dictionary for the specified entity.
    """
    project_root = Path(__file__).resolve().parents[3]
    file_path = project_root / "configs" / "entities"/f"{entity_name}.yaml"

    if not file_path.exists():
        raise FileNotFoundError(f"Entity configuration file not found: {file_path}")    

    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config
