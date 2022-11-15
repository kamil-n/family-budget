from fastapi import FastAPI
import uvicorn

import api.config
from api.db import Base, engine


Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.get("/")
async def hello_world():
    return {"Hello": "World"}


if __name__ == "__main__":
    reload = api.config.ENV == "dev"
    uvicorn.run(
        "main:app",
        host=api.config.HOST,
        port=api.config.PORT,
        reload=reload,
    )
