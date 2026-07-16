"""TODOs
- standard projects
- milestones
- awards

- the tile map (5 -> 9 -> 5, and two moon tiles)

- global parameter bonus steps

SEE RULES AT
https://officialgamerules.org/wp-content/uploads/2025/02/Terraforming-mars-rulebook.pdf
"""

from enum import Enum, auto
import typing as t

from pydantic import BaseModel


# Misc types


CorporationId = str
CardId = str
TileId = int


# Enums
# Note: should check how these enums get serialized in the API


class GlobalParameter(Enum):
    OCEAN = auto()
    OXYGEN = auto()
    TEMPERATURE = auto()


class Phase(Enum):
    # Do we need a GAME START?
    TURN_ORDER = auto()
    RESEARCH = auto()
    ACTION = auto()
    PRODUCTION = auto()
    FINAL_PRODUCTION = auto()
    FINAL_GREENERY = auto()


class Resource(Enum):
    MEGA_CREDITS = auto()
    STEEL = auto()
    TITANIUM = auto()
    PLANT = auto()
    ENERGY = auto()
    HEAT = auto()
    # Animal? Microbe?


class TileType(Enum):
    CITY = auto()
    GREENERY = auto()
    OCEAN = auto()
    SPECIAL = auto()


class Tag(Enum):
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


class Trigger(Enum):
    AFTER_CARD_PLAY = auto()
    AFTER_TILE_PLAY = auto()


# Game state


class CardState(BaseModel):
    num_resources: int
    action_used: bool
    resources_can_be_taken: bool


class PlayerState(BaseModel):
    corporation: CorporationId | None
    hand: list[CardId]
    tableau: t.MutableMapping[CardId, CardState]
    production: t.MutableMapping[Resource, int]
    resources: t.MutableMapping[Resource, int]
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
    all_cards: t.Collection[CardId]
    deck: t.Sequence[CardId]
    player_state: list[PlayerState]
    board_state: t.MutableMapping[TileId, TileState]
    generation_state: GenerationState
    global_parameter_targets: t.MutableMapping[GlobalParameter, float]
    global_parameter_progress: t.MutableMapping[GlobalParameter, float]
    cur_generation: int

    @classmethod
    def new(
        cls,
        num_players: int,
        card_ids: t.Collection[CardId],
        tile_ids: t.Collection[TileId],
    ) -> "GameState":
        return GameState(
            all_cards=card_ids,
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


class Corporation(BaseModel):
    # TODO: How to factor in, e.g., greeneries are cheaper?
    tags: list[Tag]
    action: t.Callable[[GameState, int], GameState]
    passive_effect: t.Callable[[GameState, int], GameState]
    triggered_effect: t.Callable[[Trigger], t.Callable[[GameState, int], GameState]]


class Card(BaseModel):
    cost: int
    tags: list[Tag]
    requirements: t.Callable[[GameState, int], bool]
    action: t.Callable[[GameState, int], GameState]
    immediate_effect: t.Callable[[GameState], GameState]
    passive_effect: t.Callable[[GameState, int], GameState]
    triggered_effect: t.Callable[[Trigger], t.Callable[[GameState, int], GameState]]
    victory_points: t.Callable[[PlayerState], int]


class Tile(BaseModel):
    adjacent: list[TileId]  # or list tile?
    name: str | None
    bonuses: list[Resource]
    isReservedForOcean: bool
