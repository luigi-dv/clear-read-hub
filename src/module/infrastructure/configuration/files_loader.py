import os
import yaml


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        for key, value in self.items():
            if isinstance(value, dict):
                self[key] = AttrDict(value)
        self.__dict__ = self


def load_messages(file_path="files/messages.yaml"):
    """
    Load a messages YAML file
        :param file_path:
        :return: Dictionary with the data
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(current_dir, file_path)

    with open(config_path, encoding="utf-8") as file:
        data = yaml.load(file, Loader=yaml.FullLoader)

    return AttrDict(data)


def load_responses(file_path="files/responses.yaml"):
    """
    Load a response YAML file
        :param file_path:
        :return: Dictionary with the data
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(current_dir, file_path)

    with open(config_path, encoding="utf-8") as file:
        data = yaml.load(file, Loader=yaml.FullLoader)

    return AttrDict(data)
