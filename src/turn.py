import langchain
import interlab
import random

from datastore import get_characters, get_character_orbit
from logging_config import logger
from logging_extras import log_the_world_so_far, format_character_list_for_logs
from schema import Character
from upkeep import check_for_new_elements

gpt35 = langchain.chat_models.ChatOpenAI(model_name='gpt-3.5-turbo-1106')
gpt4turbo = langchain.chat_models.ChatOpenAI(model_name='gpt-4-1106-preview')

NUM_CHARACTERS_ACTING_PER_TURN = 2

# (before turn)
# - load characters, locations, relations

# - load setting and create base agent?
#   - TBD: new base agent per turn? or per LLM action?
DIRECTOR_BASE_PROMPT = """
You are a creative mastermind building a world and designing and directing the characters within it.

You thrive on creativity and a bit of spice, but also feel strongly that worlds should make sense and be realistic, pragmatic, and fleshed out to be as whole as possible. The little details (who provides the services that make the settlement work, what are those services, where do people eat, drink, and live -- e.g. where does the wife of the night janitor for the space port go to buy coffee and donuts, and who is the barista's childhood friend? (NOTE: these are examples, not instructions)) matter as much as the grand stories (major crises or events). In other words, the NPCs and their lives, locations, and relations, matter as much as the protagonists of the story.
"""

def do_daily_turn():

    logger.info("## BEGINNING TURN!")
    log_the_world_so_far()

    # iterate through characters
    # - each character "interacts" with 1-2+ locations and 0-2+ other characters
    #   - random selection of target location(s)|character(s) -> do in python initially? (or ask LLM to choose based on weighting?)
    #   ---- TBD: decide|ask whether it's an unusual day or typical day for this character. Also good day | bad day?

    #   - ask LLM to narrate the interaction (what did the character do today)

    # v0.0 experiment: just load characters and ask what they did today
    characters = get_characters()
    character_vignettes: list[(Character, str)] = []

    # for character in characters:
    selected_characters = random.choices(population=characters, k=NUM_CHARACTERS_ACTING_PER_TURN)
    logger.info(f"Today will focus on these characters:\n{format_character_list_for_logs(selected_characters)}")

    for character in selected_characters:
        logger.info(f"### Zooming in on character: **{character.name}**")
        character_orbit = get_character_orbit(character)
        logger.debug("character_orbit")
        logger.debug(character_orbit)
        
        # refresh the director LLM to avoid confusion between characters
        fearless_director = interlab.actor.OneShotLLMActor(
            name="FearlessDirector",
            # model=gpt35,
            model=gpt4turbo,
            system_prompt=DIRECTOR_BASE_PROMPT,
        )

        # A NEW DAY DAWNS
        # TODO: daily hooks could go here
        DAILY_INFO_HOOK = """
        ## DAY 12
        It is a typical tuesday. There is a chance of rain in the afternoon.
        """
        fearless_director.observe(DAILY_INFO_HOOK)

        fearless_director.observe(
            f"We turn our attention to the story of {character.name}"
        )
        fearless_director.observe(
            f""" --- {character.name} ---
            {character_orbit}"""
        )
        
        character_vignette = fearless_director.query("Write a very short plot synopsis of an interesting episode in which this character appears")
        # character_vignette = fearless_director.query("Tell a story about what this character did today, where they went, who they met, etc.")
        # character_vignette = fearless_director.query("Describe what this character did today, where they went, who they met, etc. Narrate 2-3 short vignettes at different times of day (e.g. morning, afternoon, evening, night).")

        logger.info(f"#### Director generated new vignette!\n{character_vignette}")
        character_vignettes.append((character, character_vignette))
        check_for_new_elements(character_vignette)
        exit()
    
    # after all vignettes have been created, analyze them for new characters, etc
    new_characters: list[Character] = []
    for (character, vignette) in character_vignettes:
        new_characters += check_for_new_elements(vignette)
    
            

# def do_daily_turns(
#     num_turns: int = 1,
# ):
#     for day_n in range(1, num_turns+1):
#         do_turn()
#     logger.info("# DAY (turn) RESULTS")
#     logger.info("## PUBLISHING NEW VIGNETTES")
#     for character, vignette in character_vignettes:
#         logger.info(f"""
#             ### {character.name}
#             {vignette}
#         """)
            
#     logger.info("## NEW CHARACTERS RECORDED")
#     for character in new_characters:
#         logger.info(f"""
#             ### {character.name}
#             {character.description}
#         """)