import json
import logging
from pathlib import Path

# from data.characters import all_characters
from data.locations import all_locations
from data.relations import all_relations
from schema import Character, Location, Relation

THIS_FILE_DIR = Path(__file__).parent.resolve()
DATA_DIR = THIS_FILE_DIR / "data"
CHARACTER_DIR = DATA_DIR / "characters"

# -------------- CHARACTER -----------------
def get_characters(
    id_in: list[str] | None = None,
    name_in: list[str] | None = None,
) -> list[Character]:
    characters: list[Character] = []
    character_filepaths = CHARACTER_DIR.glob("*.json")
    for filepath in character_filepaths:
        logging.debug(f"Loading character from: {filepath}")
        with open(filepath) as f:
            data = json.load(f)
        characters.append(Character(**data))

    if id_in is not None:
        characters = [
            c for c in characters
            # if c["id"] in id_in
            if c.id in id_in
        ]
    if name_in is not None:
        characters = [
            c for c in characters
            # if c["name"] in name_in
            if c.name in name_in
        ]

    return characters
    # return [Character(**c) for c in characters]


def get_character(
    id: str
) -> Character | None:
    filepath = CHARACTER_DIR / f"{id}.json"
    logging.debug(f"Loading character from: {filepath}")
    if not filepath.exists():
        logging.warning(f"{filepath} not found.")
        return None
    with open(filepath) as f:
        data = json.load(f)
    return Character(**data)


def save_character(
    character: Character,
) -> Character:
    filepath = CHARACTER_DIR / f"{character.id}.json"
    logging.debug(f"Saving character to: {filepath}")
    with open(filepath, "w") as file:
        json.dump(
            character.__dict__,
            file,
            ensure_ascii=False,
            indent=4,
        )
    

# -------------- LOCATION -----------------
def get_locations(
    id_in: list[str] | None = None,
    name_in: list[str] | None = None,
) -> list[Location]:
    locations = all_locations
    if id_in is not None:
        locations = [
            l for l in locations
            if l.id in id_in
        ]
    if name_in is not None:
        locations = [
            l for l in locations
            if l.name in name_in
        ]
    # return locations
    return [Location(**l) for l in all_locations]

def get_location(
    id: str
) -> Location | None:
    matching_locations = [
        l for l in all_locations
            if l["id"] == id
    ]
    if len(matching_locations) == 0:
        return None
    # return matching_locations[0]
    return Location(**matching_locations[0])


# -------------- RELATION -----------------
def get_relations(
    x_node_id: str | None = None,
    # name_in: list[str] | None = None,
) -> list[Relation]:
    relations = all_relations
    if x_node_id is not None:
        relations = [
            r for r in relations
            if r["x_node_id"] == x_node_id
        ]

    return [Relation(**r) for r in relations]