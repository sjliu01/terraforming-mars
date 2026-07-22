from fastapi import FastAPI
from game_manager import GameManager
from game_types import GameState
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
