import datastore
from logging_config import logger
from schema import Character, Location, Relation

def format_character_list_for_logs(characters: list[Character]) -> None:
    return "\n".join([
        f"- **{c.name}**: {c.description}" for c in characters
    ])

def format_location_list_for_logs(locations: list[:Location]) -> None:
    return "\n".join([
        f"- **{l.name}**: {l.description}" for l in locations
    ])

def format_relation_list_for_logs(relations: list[Relation]) -> None:
    return "\n".join([
        f"- ({r.x_node_type}:**{r.x_node_id}**)->({r.y_node_type}:**{r.y_node_id}**): {r.description}" for r in relations
    ])

def log_the_world_so_far() -> None:
    logger.info("### The world so far:")
    characters = datastore.get_characters()
    logger.info(f"#### CHARACTERS\n{format_character_list_for_logs(characters)}")
    
    locations = datastore.get_locations()
    logger.info(f"#### LOCATIONS\n{format_location_list_for_logs(locations)}")
    
    relations = datastore.get_relations()
    logger.info(f"#### RELATIONS\n{format_relation_list_for_logs(relations)}")