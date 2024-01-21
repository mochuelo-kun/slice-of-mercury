import logging

# from interlab.actor.base import ActorBase
import langchain
import interlab
from pydantic.dataclasses import dataclass, Field

from datastore import (
    get_characters,
    save_character,
    get_locations,
    save_location,
    get_relations,
    save_relation,
)
from schema import Character, Location, Relation
from util import str_to_safe_id

gpt35 = langchain.chat_models.ChatOpenAI(model_name='gpt-3.5-turbo-1106')
gpt4turbo = langchain.chat_models.ChatOpenAI(model_name='gpt-4-1106-preview')

ARCHIVIST_EDITOR_PROMPT = """You are an archivist trying to keep up a database directory of information about characters, locations, relations, etc. in a fictional world. Your job is to review new vignettes written by the creative director, log any new elements, and give feedback when new elements conflict with existing ones."""


@dataclass
class NewElementsCheck:
    new_characters: list[Character] = Field(
        description="List of any new characters from the NEW_STORY_VIGNETTE (above) that are not already in the EXISTING_CHARACTER_LIST (above)"
    )
    new_locations: list[Location] = Field(
        description="List of any new locations from the NEW_STORY_VIGNETTE (above) that are not already in the EXISTING_LOCATION_LIST (above)"
    )
    new_relations: list[Relation] = Field(
        description="List of any new relations from the NEW_STORY_VIGNETTE (above) that are not already in the EXISTING_RELATION_LIST (above)"
    )

def check_for_new_characters(
    # actor: interlab.actor.ActorBase,
    vignette: str,
# ) -> list[Character]:
) -> list[NewElementsCheck]:
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
        expected_type=NewElementsCheck,
    )

    logging.info("new_elements_check_results")
    logging.info(new_elements_check_results)

    # logging.info("new_elements_check_results.data")
    # logging.info(new_elements_check_results.data)

    # TODO save the new data
    # exit()

    if len(new_elements_check_results.new_characters) == 0:
        logging.info("No new characters detected.")
        return []
    else:
        new_characters = new_elements_check_results.new_characters
        for character in new_characters:
            logging.info("### New character detected!")
            logging.info(character)
            
            # quick ID formatting check
            expected_id = str_to_safe_id(character.name)
            if character.id != expected_id:
                logging.warning(f"LLM generated ID ({character.id}) does not match expected ID form ({expected_id}). Overwriting to expected.")
                character.id = expected_id
            
            # TODO/TBD: move saving to safer location?
            save_character(character)
    
    if len(new_elements_check_results.new_locations) == 0:
        logging.info("No new locations detected.")
        return []
    else:
        new_locations = new_elements_check_results.new_locations
        for location in new_locations:
            logging.info("### New location detected!")
            logging.info(location)
            
            # quick ID formatting check
            expected_id = str_to_safe_id(location.name)
            if location.id != expected_id:
                logging.warning(f"LLM generated ID ({location.id}) does not match expected ID form ({expected_id}). Overwriting to expected.")
                location.id = expected_id
            
            # TODO/TBD: move saving to safer location?
            save_location(location)
        
    if len(new_elements_check_results.new_relations) == 0:
        logging.info("No new relations detected.")
        return []
    else:
        new_relations = new_elements_check_results.new_relations
        for relation in new_relations:
            logging.info("### New relation detected!")
            logging.info(relation)

            # TODO: do we need to double check that node IDs are real?
            
            # TODO/TBD: move saving to safer relation?
            save_relation(relation)
        
    
    # return new_character_check_results.data


# TODO: how to make a "does this all make sense/cohere" check?