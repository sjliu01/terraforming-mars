import json
import os

from game_types import CardDescription, CorporationDescription, TileDescription

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


def get_cards() -> list[CardDescription]:
    with open(os.path.join(DATA_DIR, "cards.json")) as f:
        return json.load(f)


def get_corporations() -> list[CorporationDescription]:
    with open(os.path.join(DATA_DIR, "corporations.json")) as f:
        return json.load(f)


def get_tiles() -> list[TileDescription]:
    with open(os.path.join(DATA_DIR, "tiles.json")) as f:
        return json.load(f)
