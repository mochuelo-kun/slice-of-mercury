import json
from pathlib import Path

from logging_config import logger
from schema import (
    Character,
    CharacterOrbit,
    Location,
    Relation,
    CHARACTER_NODE_TYPE,
    LOCATION_NODE_TYPE,
)

THIS_FILE_DIR = Path(__file__).parent.resolve()
DATA_DIR = THIS_FILE_DIR / "data"
CHARACTER_DIR = DATA_DIR / "characters"
LOCATION_DIR = DATA_DIR / "locations"
RELATION_DIR = DATA_DIR / "relations"

# -------------- CHARACTER -----------------
def get_characters(
    id_in: list[str] | None = None,
    name_in: list[str] | None = None,
) -> list[Character]:
    characters: list[Character] = []
    character_filepaths = CHARACTER_DIR.glob("*.json")
    for filepath in character_filepaths:
        logger.debug(f"Loading character from: {filepath}")
        with open(filepath) as f:
            data = json.load(f)
        characters.append(Character(**data))

    if id_in is not None:
        characters = [
            c for c in characters
            if c.id in id_in
        ]
    if name_in is not None:
        characters = [
            c for c in characters
            if c.name in name_in
        ]

    return characters


def get_character(
    id: str
) -> Character | None:
    filepath = CHARACTER_DIR / f"{id}.json"
    logger.debug(f"Loading character from: {filepath}")
    if not filepath.exists():
        logger.warning(f"{filepath} not found.")
        return None
    with open(filepath) as f:
        data = json.load(f)
    return Character(**data)


def save_character(
    character: Character,
) -> Character:
    filepath = CHARACTER_DIR / f"{character.id}.json"
    logger.debug(f"Saving character to: {filepath}")
    with open(filepath, "w") as file:
        json.dump(
            character.__dict__,
            file,
            ensure_ascii=False,
            indent=4,
        )

def save_characters(characters: list[Character]) -> list[Character]:
    for character in characters:
        save_character(character)
    

# -------------- LOCATION -----------------
def get_locations(
    id_in: list[str] | None = None,
    name_in: list[str] | None = None,
) -> list[Location]:
    # locations = all_locations
    locations: list[Location] = []
    location_filepaths = LOCATION_DIR.glob("*.json")
    for filepath in location_filepaths:
        logger.debug(f"Loading location from: {filepath}")
        with open(filepath) as f:
            data = json.load(f)
        locations.append(Location(**data))
    
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
    return locations

def get_location(
    id: str
) -> Location | None:
    filepath = LOCATION_DIR / f"{id}.json"
    logger.debug(f"Loading location from: {filepath}")
    if not filepath.exists():
        logger.warning(f"{filepath} not found.")
        return None
    with open(filepath) as f:
        data = json.load(f)
    return Location(**data)

def save_location(
    location: Location,
) -> Location:
    filepath = LOCATION_DIR / f"{location.id}.json"
    logger.debug(f"Saving location to: {filepath}")
    with open(filepath, "w") as file:
        json.dump(
            location.__dict__,
            file,
            ensure_ascii=False,
            indent=4,
        )

def save_locations(locations: list[Location]) -> list[Location]:
    for location in locations:
        save_location(location)


# -------------- RELATION -----------------
def get_relations(
    x_node_id_eq: str | None = None,
    # name_in: list[str] | None = None,
) -> list[Relation]:
    relations: list[Relation] = []
    relation_filepaths = RELATION_DIR.glob("*.json")
    for filepath in relation_filepaths:
        logger.debug(f"Loading relation from: {filepath}")
        with open(filepath) as f:
            data = json.load(f)
        relations.append(Relation(**data))

    logger.debug("all relations")
    logger.debug(relations)
    if x_node_id_eq is not None:
        logger.debug(f"filter for x_node_id_eq={x_node_id_eq}")
        logger.debug(str([
            (r.x_node_id, r.x_node_id == x_node_id_eq)
            for r in relations
        ]))
        relations = [
            r for r in relations
            if r.x_node_id == x_node_id_eq
        ]
        logger.debug(f"filtered {relations}")
    return relations

def save_relation(
    relation: Relation,
) -> Relation:
    filepath = RELATION_DIR / f"{relation.x_node_id}--{relation.y_node_id}.json"
    logger.debug(f"Saving relation to: {filepath}")
    with open(filepath, "w") as file:
        json.dump(
            relation.__dict__,
            file,
            ensure_ascii=False,
            indent=4,
        )

def save_relations(relations: list[Relation]) -> list[Relation]:
    for relation in relations:
        save_relation(relation)


# -------------- CHARACTER ORBIT -----------------

def get_character_orbit(
    character: Character,
    # depth: int = 1,
) -> CharacterOrbit:
    relations = get_relations(
        x_node_id_eq=character.id,
    )
    related_character_ids: list[str] = [
        r.y_node_id for r in relations
        if r.y_node_type == CHARACTER_NODE_TYPE
    ]
    related_characters = get_characters(
        id_in=related_character_ids,
    )
    related_location_ids: list[str] = [
        r.y_node_id for r in relations
        if r.y_node_type == LOCATION_NODE_TYPE
    ]
    related_locations = get_locations(
        id_in=related_location_ids,
    )
    return CharacterOrbit(
        character=character,
        relations=relations,
        related_characters=related_characters,
        related_locations=related_locations,
    )
