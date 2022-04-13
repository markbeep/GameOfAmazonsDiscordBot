import json
from types import SimpleNamespace


def get_config():
    """Returns the config as one big object
    """
    with open("config.json", "r") as f:
        return json.load(f, object_hook=lambda d: SimpleNamespace(**d))
