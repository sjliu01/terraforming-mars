import typing as t

from game_types import GameState
from game_types import Corporation
from game_types import Card
from game_types import Tile
from game_types import CorporationId
from game_types import CardId
from game_types import TileId


def load_corporations() -> dict[CorporationId, Corporation]:
    return {}


def load_cards() -> dict[CardId, Card]:
    return {}


def load_tiles() -> dict[TileId, Tile]:
    return {}


class GameManager:
    # TODO: Add all the methods to handle different actions / flow of game / etc

    def __init__(
        self,
        state: GameState,
        corporations: t.Mapping[CorporationId, Corporation],
        cards: t.Mapping[CardId, Card],
        tiles: t.Mapping[TileId, Tile],
    ):
        self.state = state
        self.corporations = corporations
        self.cards = cards
        self.tiles = tiles

    @classmethod
    def initialize_new_game(
        cls,
        num_players: int,
        corporations: t.Mapping[CorporationId, Corporation] | None = None,
        cards: t.Mapping[CardId, Card] | None = None,
        tiles: t.Mapping[TileId, Tile] | None = None,
    ) -> "GameManager":
        if corporations is None:
            corporations = load_corporations()

        if cards is None:
            cards = load_cards()

        if tiles is None:
            tiles = load_tiles()

        return GameManager(
            state=GameState.new(
                num_players,
                cards.keys(),
                tiles.keys(),
            ),
            corporations=corporations,
            cards=cards,
            tiles=tiles,
        )

    @classmethod
    def load_game(cls):
        pass
