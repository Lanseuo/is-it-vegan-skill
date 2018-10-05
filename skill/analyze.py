import json
import os
from pathlib import Path


def get_status_items():
    path = Path(os.path.dirname(os.path.realpath(__file__))).parent
    for status in ["vegan", "can_be_vegan", "non_vegan"]:
        with open(path / "items" / (status + ".json"), "r") as f:
            items = json.load(f)
        yield status, items


def match(item, search_item):
    search_item = search_item.lower()

    if item["name"].lower() == search_item:
        return True

    if search_item in map(lambda i: i.lower(), item.get("synonyms", [])):
        return True

    return False


def check(search_item):
    for (status, items) in get_status_items():
        for item in items:
            if match(item, search_item):
                return {"status": status, **item}

    return None
