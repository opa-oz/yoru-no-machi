from pathlib import Path

import yaml

from models import Config


def get_config(directory=Path.cwd()) -> Config:
    # Load yaml file
    with open(directory / 'config.yaml', 'r') as config_file:
        loaded_config = yaml.safe_load(config_file)

    # Parse and validate with Pydantic
    config = Config(**loaded_config)

    return config
