import os
import yaml


def load_config(file_path="config/settings.yaml"):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(current_dir, file_path)

    with open(config_path, encoding="utf-8") as file:
        config_data = yaml.load(file, Loader=yaml.FullLoader)

    return config_data
