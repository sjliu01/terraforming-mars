from enum import Enum, auto
import typing as t

from pydantic import BaseModel


# Misc types


CorporationId = str
CardId = str
TileId = int


# Enums
# Note: should check how these enums get serialized in the API


class EnvironmentMetric(Enum):
    OCEANS = auto()
    OXYGEN = auto()
    TEMPERATURE = auto()


class Phase(Enum):
    DRAW = auto()
    PLAY = auto()
    PRODUCTION = auto()
    FINAL_PRODUCTION = auto()
    FINAL_GREENERY = auto()


class Resource(Enum):
    MC = auto()
    STEEL = auto()
    TITANIUM = auto()
    PLANT = auto()
    ENERGY = auto()
    HEAT = auto()


class TileType(Enum):
    CITY = auto()
    GREENERY = auto()
    OCEAN = auto()
    SPECIAL = auto()


class Tag(Enum):
    ANIMAL = auto()
    BUILDING = auto()
    EARTH = auto()
    JUPITER = auto()
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
    num_counters: int
    action_used: bool
    counters_can_be_taken: bool


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


class RoundState(BaseModel):
    phase: Phase
    first_to_play: int
    passed_this_round: list[bool]

    @classmethod
    def new(cls, num_players: int, first_to_play: int = 0) -> "RoundState":
        return RoundState(
            phase=Phase.DRAW,
            first_to_play=first_to_play,
            passed_this_round=[False] * num_players,
        )


class GameState(BaseModel):
    all_cards: t.Collection[CardId]
    deck: t.Sequence[CardId]
    player_state: list[PlayerState]
    board_state: t.MutableMapping[TileId, TileState]
    round_state: RoundState
    environment_targets: t.MutableMapping[EnvironmentMetric, float]
    environment_progress: t.MutableMapping[EnvironmentMetric, float]
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
            round_state=RoundState.new(num_players),
            environment_targets={
                EnvironmentMetric.TEMPERATURE: 8,
                EnvironmentMetric.OXYGEN: 14,
                EnvironmentMetric.OCEANS: 9,
            },
            environment_progress={
                EnvironmentMetric.TEMPERATURE: -30,
                EnvironmentMetric.OXYGEN: 0,
                EnvironmentMetric.OCEANS: 0,
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
    tags: list[Tag]
    action: t.Callable[[GameState, int], GameState]
    requirements: t.Callable[[GameState, int], bool]
    passive_effect: t.Callable[[GameState, int], GameState]
    triggered_effect: t.Callable[[Trigger], t.Callable[[GameState, int], GameState]]
    victory_points: t.Callable[[PlayerState], int]


class Tile(BaseModel):
    adjacent: list[TileId]  # or list tile?
    name: str | None
    bonuses: list[Resource]
    isReservedForOcean: bool
