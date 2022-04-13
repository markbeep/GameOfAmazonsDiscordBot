import os
import json


def create_files():
    if not os.path.exists("config.json"):
        with open("config.json", "w") as f:
            json.dump({"config": "", "prefixes": ["placeholder"]}, f, indent=4)
        print("Created config.json")
