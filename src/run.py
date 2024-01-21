import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

import dotenv
dotenv.load_dotenv()

from logging_config import logger
from turn import play_rounds

def start():
    logger.info("# STARTING a new run")
    play_rounds()