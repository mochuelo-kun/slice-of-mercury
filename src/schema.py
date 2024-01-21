from pydantic import BaseModel, Field
from typing import Optional, Literal

# -------------- CHARACTER -----------------
class Character(BaseModel):
    # TODO: ensure ID matches expected pattern somewhere?
    id: str
    name: str = Field(description="Full name of this character")
    description: str = Field(description="Core description of this character")

    # tidbits?
    # knowledge? or get_recent_memory?


# -------------- LOCATION -----------------
class Location(BaseModel):
    id: str
    name: str
    description: str
    
    # tidbits?


# -------------- RELATION -----------------

CHARACTER_NODE_TYPE = Literal["character"]
LOCATION_NODE_TYPE = Literal["location"]

# UNIDIRECTIONAL = Literal["uni"]
# BIDIRECTIONAL = Literal["bi"]

class Relation(BaseModel):
    # id: str # just use name as ID for now?
    # name: str

    x_node_id: str
    x_node_type: Literal[CHARACTER_NODE_TYPE, LOCATION_NODE_TYPE]
    y_node_id: str
    y_node_type: Literal[CHARACTER_NODE_TYPE, LOCATION_NODE_TYPE]

    # direction: Literal[UNIDIRECTIONAL, BIDIRECTIONAL]
    description: str

    # relation_type?
    # strength?

    # def x_node() -> Character | Location:
    #     if x_node_type == CHARACTER_NODE_TYPE:
    #         return 
