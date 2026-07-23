import data_loader
from fastapi import FastAPI
from game_manager import GameManager
from game_types import (
    CardDescription,
    CorporationDescription,
    GameState,
    TileDescription,
)
from pydantic import BaseModel

app = FastAPI()


class MessageResponse(BaseModel):
    message: str


@app.get(
    "/api/message/",
    response_model=MessageResponse,
)
async def get_message():
    return MessageResponse(message="peepeepoopoo")


@app.get(
    "/api/state/init",
    response_model=GameState,
)
async def get_initial_game_state():
    manager = GameManager.initialize_new_game(2)
    return manager.state


@app.get(
    "/api/data/cards/",
    response_model=list[CardDescription],
)
async def get_cards():
    return data_loader.get_cards()


@app.get(
    "/api/data/corporations/",
    response_model=list[CorporationDescription],
)
async def get_corporations():
    return data_loader.get_corporations()


@app.get(
    "/api/data/tiles/",
    response_model=list[TileDescription],
)
async def get_tiles():
    return data_loader.get_tiles()
