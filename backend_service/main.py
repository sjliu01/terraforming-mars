from fastapi import FastAPI

from game_manager import GameManager
from game_types import GameState

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "peepeepoopoo"}

@app.get(
    "/api/state/init",
    response_model=GameState,
)
async def get_initial_game_state():
    manager = GameManager.initialize_new_game(2)
    return manager.state
