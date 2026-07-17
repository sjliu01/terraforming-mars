from fastapi import FastAPI
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
