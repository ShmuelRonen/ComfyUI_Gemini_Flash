import os
import json

config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "config.json")

# Create config if it doesn't exist or is empty/invalid
if not os.path.isfile(config_path) or os.path.getsize(config_path) == 0:
    config = {
        "GEMINI_API_KEY": "your key",
        "PROXY": ""
    }
    with open(config_path, "w") as f:
        json.dump(config, f, indent=4)

# Load config
try:
    with open(config_path, "r") as f:
        config = json.load(f)
except json.JSONDecodeError:
    config = {
        "GEMINI_API_KEY": "your key",
        "PROXY": ""
    }
    with open(config_path, "w") as f:
        json.dump(config, f, indent=4)

from .Gemini_Flash_Node import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']