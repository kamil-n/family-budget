from fastapi import FastAPI
import uvicorn

from api.config import ENV, HOST, PORT
from api.db import Base, engine
from api.routers import user, budget, token


Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(user.router, tags=['Users'])
app.include_router(budget.router, tags=['Readings'])
app.include_router(token.router, tags=['Token'])


if __name__ == "__main__":
    reload = ENV == "dev"
    uvicorn.run("main:app", host=HOST, port=PORT, reload=reload)
