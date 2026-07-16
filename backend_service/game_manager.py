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

    @classmethod
    def end_game(cls):
        """
        Count up all the points for all players
        For each player
        + Terraform rating
        + Victory points on cards
        + Victory points on cards via tokens
        + Awards 
        + Milestones
        + Greeneries
        + Cities adjacent to greeneries
        """
        players = [player for _ in self.state.player_state]
        board_state = self.state.board_state
        player_points = {p:0 for p in players}
        for p in players:
            # terraform rating
            player_points[p] += p.terraform_rating

            # Victory points on cards
            player_points[p] += sum([card_state.num_counters // card_state.divisor for card_state in p.tableau.values()])

            # Look at cards. Add up points
            # ..


            
