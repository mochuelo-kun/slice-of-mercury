import langchain
import interlab
from pydantic.dataclasses import dataclass, Field

from datastore import (
    get_characters,
    save_characters,
    get_locations,
    save_locations,
    get_relations,
    save_relations,
)
from logging_config import logger
from logging_extras import (
    format_character_list_for_logs,
    format_location_list_for_logs,
    format_relation_list_for_logs,
)
from schema import Character, Location, Relation
from util import str_to_safe_id

gpt35 = langchain.chat_models.ChatOpenAI(model_name='gpt-3.5-turbo-1106')
gpt4turbo = langchain.chat_models.ChatOpenAI(model_name='gpt-4-1106-preview')

ARCHIVIST_EDITOR_PROMPT = """You are an archivist trying to keep up a database directory of information about characters, locations, relations, etc. in a fictional world. Your job is to review new vignettes written by the creative director, log any new elements, and give feedback when new elements conflict with existing ones."""

def normalize_character_ids(characters: list[Character]) -> list[Character]:
    normalized_characters: list[Character] = []
    for character in characters:
        expected_id = str_to_safe_id(character.name)
        if character.id != expected_id:
            logger.debug(f"LLM generated ID ({character.id}) does not match expected ID form ({expected_id}). Overwriting to expected.")
            character.id = expected_id
        normalized_characters.append(character)
    return normalized_characters

def normalize_location_ids(locations: list[Location]) -> list[Location]:
    normalized_locations: list[location] = []
    for location in locations:
        # quick ID formatting check
        expected_id = str_to_safe_id(location.name)
        if location.id != expected_id:
            logger.debug(f"LLM generated ID ({location.id}) does not match expected ID form ({expected_id}). Overwriting to expected.")
            location.id = expected_id
        normalized_locations.append(location)
    return normalized_locations

@dataclass
class NewElementsAnalysis:
    new_characters: list[Character] = Field(
        description="List of any new characters from the NEW_STORY_VIGNETTE (above) that are not already in the EXISTING_CHARACTER_LIST (above)"
    )
    new_locations: list[Location] = Field(
        description="List of any new locations from the NEW_STORY_VIGNETTE (above) that are not already in the EXISTING_LOCATION_LIST (above)"
    )
    new_relations: list[Relation] = Field(
        description="List of any new relations from the NEW_STORY_VIGNETTE (above) that are not already in the EXISTING_RELATION_LIST (above)"
    )

def check_for_new_elements(
    # actor: interlab.actor.ActorBase,
    vignette: str,
) -> NewElementsAnalysis:
    logger.info("### Checking story vignette for new world elements...")

    # TODO stronger input type, e.g. Event? Vignette?
    archivist_editor = interlab.actor.OneShotLLMActor(
        name="ArchivistEditor",
        # model=gpt35,
        model=gpt4turbo,
        system_prompt=ARCHIVIST_EDITOR_PROMPT,
    )

    existing_characters = get_characters()
    existing_locations = get_locations()
    existing_relations = get_relations()

# The following is a list of characters we have recorded in the official database so far:
    archivist_editor.observe(f"""
## EXISTING_CHARACTER_LIST
{existing_characters}
""")
    archivist_editor.observe(f"""
## EXISTING_LOCATION_LIST
{existing_locations}
""")
    archivist_editor.observe(f"""
## EXISTING_RELATIONS_LIST
{existing_relations}
""")
    
    archivist_editor.observe(f"""## NEW_STORY_VIGNETTE
    {vignette}
""")
    new_elements_check_results = archivist_editor.query(
        "Did any new characters, locations, or relations that are not catalogued in the directory yet appear in the latest vignette? If so please format what we know about them for the directory. If the character does not have a full name, please create one for them, using a similar style to existing names.",
        expected_type=NewElementsAnalysis,
    )

    logger.debug("new_elements_check_results")
    logger.debug(new_elements_check_results)

    if len(new_elements_check_results.new_characters) == 0:
        logger.info("No new characters detected.")
    else:
        new_characters = new_elements_check_results.new_characters
        new_characters = normalize_character_ids(new_characters)
        logger.info(f"New characters detected!\n{format_character_list_for_logs(new_characters)}")
        save_characters(new_characters)    
    
    if len(new_elements_check_results.new_locations) == 0:
        logger.info("No new locations detected.")
    else:
        new_locations = new_elements_check_results.new_locations
        new_locations = new_elements_check_results.new_locations
        new_locations = normalize_location_ids(new_locations)
        logger.info(f"New locations detected!\n{format_location_list_for_logs(new_locations)}")
        # TODO/TBD: move saving to safer location?
        save_locations(new_locations)
        
    if len(new_elements_check_results.new_relations) == 0:
        logger.info("No new relations detected.")
    else:
        new_relations = new_elements_check_results.new_relations
        new_relations = new_elements_check_results.new_relations
        # TODO: do we need to double check that node IDs are real?
        logger.info(f"New relations detected!\n{format_relation_list_for_logs(new_relations)}")
        # TODO/TBD: move saving to safer location?
        save_relations(new_relations)
        
    
    return new_elements_check_results


# TODO: how to make a "does this all make sense/cohere" check?