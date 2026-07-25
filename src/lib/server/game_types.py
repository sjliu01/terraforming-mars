"""TODOs
- standard projects
- milestones
- awards

- the tile map (5 -> 9 -> 5, and two moon tiles)

- global parameter bonus steps

SEE RULES AT
https://officialgamerules.org/wp-content/uploads/2025/02/Terraforming-mars-rulebook.pdf
"""

import typing as t
from enum import StrEnum, auto

from pydantic import BaseModel

# Misc types


CorporationId = str
CardId = str
TileId = int


# Enums
# Note: should check how these enums get serialized in the API


class GlobalParameter(StrEnum):
    OCEAN = auto()
    OXYGEN = auto()
    TEMPERATURE = auto()


class Phase(StrEnum):
    # Do we need a GAME START?
    TURN_ORDER = auto()
    RESEARCH = auto()
    ACTION = auto()
    PRODUCTION = auto()
    FINAL_PRODUCTION = auto()
    FINAL_GREENERY = auto()


class Resource(StrEnum):
    MEGA_CREDITS = auto()
    STEEL = auto()
    TITANIUM = auto()
    PLANT = auto()
    ENERGY = auto()
    HEAT = auto()
    # Animal? Microbe?


class TileType(StrEnum):
    CITY = auto()
    GREENERY = auto()
    OCEAN = auto()
    SPECIAL = auto()


class Tag(StrEnum):
    ANIMAL = auto()
    BUILDING = auto()
    CITY = auto()
    EARTH = auto()
    EVENT = auto()
    JOVIAN = auto()
    MICROBE = auto()
    PLANT = auto()
    POWER = auto()
    SCIENCE = auto()
    SPACE = auto()


class Trigger(StrEnum):
    AFTER_CARD_PLAY = auto()
    AFTER_TILE_PLAY = auto()


class Planet(StrEnum):
    MARS = auto()
    PHOBOS = auto()
    GANYMEDE = auto()


class Version(StrEnum):
    BASE = auto()
    CORPORATE_ERA = auto()


# Game state


class CardState(BaseModel):
    num_resources: int
    action_used: bool
    resources_can_be_taken: bool


class PlayerState(BaseModel):
    corporation: CorporationId | None
    hand: list[CardId]
    tableau: dict[CardId, CardState]
    production: dict[Resource, int]
    resources: dict[Resource, int]
    terraform_rating: int

    @classmethod
    def new(cls) -> "PlayerState":
        return PlayerState(
            corporation=None,
            hand=[],
            tableau={},
            production={resource: 0 for resource in Resource},
            resources={resource: 0 for resource in Resource},
            terraform_rating=20,
        )

    @classmethod
    def remove_card_from_hand(cls, card_id: CardId) -> CardId:
        """
        Removes card from hand and returns the removed card Id 
        """
        if card_id not in cls.hand:
            raise
        return card_id

    @classmethod
    def add_card_to_hand(cls, card_id: CardId) -> CardId:
        cls.hand.append(card_id)
        return card_id

    @classmethod
    def add_card_to_tableau(cls, card_id: CardId, num_resources: int = 0, resources_can_be_taken: bool = False) -> CardId:
        """
        Adds a card to player's tableau and returns the added card id
        It is the callers responsibility to ensure that the card can indeed be played.
        """
        cls.tableau[card_id] = CardState(num_resources=num_resources, action_used=False, resources_can_be_taken=resources_can_be_taken)
        return card_id

    @classmethod
    def mutate_resources(cls, resources: tuple[tuple[Resource, int], ...]) -> dict[Resource, int]:
        """
        Mutate resources to player state by specified resource and amount tuple, returns the mutated player's resources 
        """
        for resource, amount in resources:
            cls.resources[resource] += amount
        return cls.resources

    @classmethod
    def mutate_terraform_rating(cls, rating_change: int) -> int:
        cls.terraform_rating += rating_change
        return cls.terraform_rating

    @classmethod
    def mutate_production(cls, production_change: tuple[tuple[Resource, int], ...]) -> dict[Resource, int]:
        """
        Mutate resource production(s) to player state by specified resource and amount tuple, returns the mutated player's resource production
        """
        for resource, amount in production_change:
            cls.production[resource] += amount
        return cls.production

    @classmethod
    def set_corporation(cls, corporation: CorporationId) -> CorporationId:
        """
        Sets the user's corporation if not already set 
        """
        if cls.corporation is None:
            cls.corporation = corporation
        return cls.corporation

class TileState(BaseModel):
    tile: TileType | None
    owner: int | None
    reserved_by: int | None

    @classmethod
    def new(cls) -> "TileState":
        return TileState(
            tile=None,
            owner=None,
            reserved_by=None,
        )


class GenerationState(BaseModel):
    phase: Phase
    first_player: int
    passed: list[bool]

    @classmethod
    def new(cls, num_players: int, first_to_play: int = 0) -> "GenerationState":
        return GenerationState(
            phase=Phase.RESEARCH,
            first_player=first_to_play,
            passed=[False] * num_players,
        )


class GameState(BaseModel):
    all_cards: list[CardId]
    deck: list[CardId]
    discards: list[CardId]
    player_state: list[PlayerState]
    board_state: dict[TileId, TileState]
    generation_state: GenerationState
    global_parameter_targets: dict[GlobalParameter, float]
    global_parameter_progress: dict[GlobalParameter, float]
    cur_generation: int

    @classmethod
    def new(
        cls,
        num_players: int,
        card_ids: t.Collection[CardId],
        tile_ids: t.Collection[TileId],
    ) -> "GameState":
        return GameState(
            all_cards=list(card_ids),
            deck=[],
            player_state=[PlayerState.new() for _ in range(num_players)],
            board_state={_id: TileState.new() for _id in tile_ids},
            generation_state=GenerationState.new(num_players),
            global_parameter_targets={
                GlobalParameter.TEMPERATURE: 8,
                GlobalParameter.OXYGEN: 14,
                GlobalParameter.OCEAN: 9,
            },
            global_parameter_progress={
                GlobalParameter.TEMPERATURE: -30,
                GlobalParameter.OXYGEN: 0,
                GlobalParameter.OCEAN: 0,
            },
            cur_generation=1,
        )


# Game objects


"""
Action categories:
    - pay X resource to get Y resource
    - pay X resource to get Y resource per city
    - pay X resource to increase requirement
        - may use titanium or steel
    - pay X production to increase terraform rating
    - pay X resource for specific action
        - reveal card see if microbe if so add resource
    - remove x resource from another card to get a resource on this card
    - one of two action options
    - pay X resource to increase production

Immediate effect categories:
    - increase x production
    - increase x production per condition of game state
    - increase x production or y production
    - place city
    - place city on specific place (tile filter)
    - place greenery on specific tile
    - place named tile
    - increase y requirement
    - decrease x production (own)
    - decrease x production (other)
    - get x resource
    - get x resource (choice between 3)
    - get x resource per condition of game state
    - add a resource to a card
    - decrease y resource self / other
    - increase production of x resource by Y or by Z if a condition is met
    - increase terraform rating

- passive effect categories
    - all cards cost one less
    - specific tags cost less
    - greeneries cost one less plant
    - requirements are flexible
    - none of your plants / microbes can get taken

- triggered effect
    - whenever any ocean is placed, get plants
    - when you play a particular tag, get resources
    - when you play a particular tag, add resource to this card
    - whenever any city is placed, get money

VP categories:
    - points per resource on card
    - points if any resource on card
    - points per specific type of adjacent tile
    - points per tag you have
    - integer points
"""


class CorporationDescription(BaseModel):
    id: int
    name: str
    tags: list[Tag]
    version: Version
    # action_description: str | None
    # passive_effect_description: str | None
    # triggered_effect_description: str | None


class Corporation(CorporationDescription):
    action: t.Callable[[GameState, int], GameState]
    passive_effect: t.Callable[[GameState, int], GameState]
    triggered_effect: t.Callable[[Trigger], t.Callable[[GameState, int], GameState]]


class CardDescription(BaseModel):
    id: int
    name: str
    base_cost: int
    tags: list[Tag]
    version: Version
    # requirements: t.Callable[[GameState, int], bool]
    # action: t.Callable[[GameState, int], GameState]
    # immediate_effect: t.Callable[[GameState], GameState]
    # passive_effect: t.Callable[[GameState, int], GameState]
    # triggered_effect: t.Callable[[Trigger], t.Callable[[GameState, int], GameState]]
    # victory_points: t.Callable[[PlayerState], int]


class Card(CardDescription):
    cost: int
    tags: list[Tag]
    requirements: t.Callable[[GameState, int], bool]
    action: t.Callable[[GameState, int], GameState]
    immediate_effect: t.Callable[[GameState], GameState]
    passive_effect: t.Callable[[GameState, int], GameState]
    triggered_effect: t.Callable[[Trigger], t.Callable[[GameState, int], GameState]]
    victory_points: t.Callable[[PlayerState], int]


class TileDescription(BaseModel):
    # We use cube coordinates for the tiles
    # See https://www.redblobgames.com/grids/hexagons/#coordinates-axial
    q: int
    r: int
    planet: Planet
    name: str | None
    resource_bonuses: list[Resource]
    card_bonuses: int
    is_reserved_for_ocean: bool


class Tile(BaseModel):
    adjacent: list[TileId]  # or list tile?
    name: str | None
    resource_bonuses: list[Resource]
    card_bonuses: int
    isReservedForOcean: bool
