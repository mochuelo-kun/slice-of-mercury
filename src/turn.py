import json

import langchain
import interlab
import random
from pydantic.dataclasses import dataclass

from datastore import get_characters, get_character_orbit
from logging_config import logger
from logging_extras import log_the_world_so_far, format_character_list_for_logs
from schema import Character, CharacterOrbit
from upkeep import check_for_new_elements, NewElementsAnalysis

gpt35 = langchain.chat_models.ChatOpenAI(model_name='gpt-3.5-turbo-1106')
gpt4turbo = langchain.chat_models.ChatOpenAI(model_name='gpt-4-1106-preview')

DEFAULT_NUM_ROUNDS = 2
DEFAULT_NUM_CHARACTERS_ACTING_PER_ROUND = 3

# (before round)
# - load characters, locations, relations

# - load setting and create base agent?
#   - TBD: new base agent per round? or per LLM action?
DIRECTOR_BASE_PROMPT = """
You are a creative mastermind building a world and designing and directing the characters within it.

You thrive on creativity and a bit of spice, but also feel strongly that worlds should make sense and be realistic, pragmatic, and fleshed out to be as whole as possible. The little details (who provides the services that make the settlement work, what are those services, where do people eat, drink, and live -- e.g. where does the wife of the night janitor for the space port go to buy coffee and donuts, and who is the barista's childhood friend? (NOTE: these are examples, not instructions)) matter as much as the grand stories (major crises or events). In other words, the NPCs and their lives, locations, and relations, matter as much as the protagonists of the story.
"""


@dataclass
class CharacterDevelopmentResult:
    character: CharacterOrbit
    vignette: str
    analysis: NewElementsAnalysis

def play_round(
    num_characters: int = DEFAULT_NUM_CHARACTERS_ACTING_PER_ROUND,
) -> list[CharacterDevelopmentResult]:

    # iterate through characters
    # - each character "interacts" with 1-2+ locations and 0-2+ other characters
    #   - random selection of target location(s)|character(s) -> do in python initially? (or ask LLM to choose based on weighting?)
    #   ---- TBD: decide|ask whether it's an unusual day or typical day for this character. Also good day | bad day?

    #   - ask LLM to narrate the interaction (what did the character do today)

    # v0.0 experiment: just load characters and ask what they did today
    characters = get_characters()
    character_vignettes: list[(Character, str)] = []

    # for character in characters:
    selected_characters = random.choices(
        population=characters,
        k=num_characters
    )
    logger.info(f"Today will focus on these characters:\n{format_character_list_for_logs(selected_characters)}")


    character_developments: list[CharacterDevelopmentResult] = []

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
        new_elements_analysis = check_for_new_elements(character_vignette)
        character_developments.append(CharacterDevelopmentResult(
            character=character_orbit,
            vignette=character_vignette,
            analysis=new_elements_analysis,
        ))
    
    # TBD move analysis and/or saving to after all vignettes have been created?
    return character_developments

def play_rounds(
    num_rounds: int = DEFAULT_NUM_ROUNDS,
):
    for round_n in range(1, num_rounds + 1):
        logger.info(f"## BEGINNING ROUND: {round_n}")
        log_the_world_so_far()
        character_developments = play_round()
        logger.info(f"### COMPLETED ROUND: {round_n}\nData results:\n```{json.dumps(character_developments.__dict__, indent=4)}```")
