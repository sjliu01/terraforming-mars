import typing as t

from game_types import Corporation, CorporationId, GameState, Tile, TileId

from lib.server.repositories.card_repository import CardRepository


def load_corporations() -> dict[CorporationId, Corporation]:
    return {}


def load_tiles() -> dict[TileId, Tile]:
    return {}


class GameManager:
    # TODO: Add all the methods to handle different actions / flow of game / etc

    def __init__(
        self,
        state: GameState,
        corporations: t.Mapping[CorporationId, Corporation],
        tiles: t.Mapping[TileId, Tile],
    ):
        self.state = state
        self.corporations = corporations
        self.tiles = tiles

    @classmethod
    def initialize_new_game(
        cls,
        num_players: int,
        corporations: t.Mapping[CorporationId, Corporation] | None = None,
        tiles: t.Mapping[TileId, Tile] | None = None,
    ) -> "GameManager":
        if corporations is None:
            corporations = load_corporations()

        if tiles is None:
            tiles = load_tiles()

        return GameManager(
            state=GameState.new(
                num_players,
                tiles.keys(),
                card_repository=CardRepository(),
            ),
            corporations=corporations,
            tiles=tiles,
        )

    @classmethod
    def load_game(cls):
        pass
