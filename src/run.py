import logging
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

import dotenv
dotenv.load_dotenv()

import datastore
from turn import do_daily_turn

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)




def start():
    logging.info("# START!")

    logging.info("## (DATA DUMP so far)")
    characters = datastore.get_characters()
    logging.info("### CHARACTERS")
    for c in characters:
        logging.info(c)
    
    locations = datastore.get_locations()
    logging.info("### LOCATIONS")
    for l in locations:
        logging.info(l)
    
    relations = datastore.get_relations()
    logging.info("### RELATIONS")
    for r in relations:
        logging.info(r)

    logging.info("## BEGINNING TURN!")
    do_daily_turn()