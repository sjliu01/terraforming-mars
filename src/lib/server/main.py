from fastapi import FastAPI

app = FastAPI()

@app.get("/api/message/")
async def root():
    return {"message": "peepeepoopoo"}
