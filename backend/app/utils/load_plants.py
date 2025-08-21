import json
import os

def load_plants():
    plants_path = os.path.join(os.path.dirname(__file__), "plants.json")
    with open(plants_path, "r", encoding="utf-8") as f:
        return json.load(f)
