from pydantic import BaseModel, Field
from typing import ForwardRef, Literal, Optional, Union

CharacterRef = ForwardRef('Character')
LocationRef = ForwardRef('Location')
RelationRef = ForwardRef('Relation')

# class Node(BaseModel):
#     id: str
#     # relations:

# -------------- CHARACTER -----------------
# class Character(Node):
class Character(BaseModel):
    # TODO: ensure ID matches expected pattern somewhere?
    id: str
    name: str = Field(description="Full name of this character")
    description: str = Field(description="Core description of this character")

    # relations: Optional[list[RelationRef]]
    # tidbits?
    # knowledge? or get_recent_memory?


# -------------- LOCATION -----------------
# class Location(Node):
class Location(BaseModel):
    id: str
    name: str
    description: str

    # relations: Optional[list[RelationRef]]
    
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
    description: str = Field(description="Description of the relation between node X and Y")
    importance: Optional[int] = Field(
        # description="A number between 1-10 (10 is high) indicating the importance of this relation to node X"
        description="A number between 1-10 (10 is high) indicating how essential this relation to node X's identity and relevance to daily life"
    )

    # x_node: Optional[CharacterRef | LocationRef]
    # y_node: Optional[CharacterRef | LocationRef]
    # x_node: Optional[Union[CharacterRef, LocationRef]]
    # y_node: Optional[Union[CharacterRef, LocationRef]]

    # relation_type?
    # strength?

    # def x_node() -> Character | Location:
    #     if x_node_type == CHARACTER_NODE_TYPE:
    #         return 


# class NodeWithNetwork()


class CharacterOrbit(BaseModel):
    character: Character
    relations: list[Relation]
    related_characters: list[Character]
    related_locations: list[Location]