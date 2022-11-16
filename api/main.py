import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from api.config import ENV, HOST, PORT
from api.db import Base, engine
from api.routers import budget, token, user

Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(user.router, tags=["Users"])
app.include_router(budget.router, tags=["Readings"])
app.include_router(token.router, tags=["Token"])


@app.get("/")
async def docs_redirect() -> RedirectResponse:
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    reload = ENV == "dev"
    uvicorn.run("main:app", host=HOST, port=PORT, reload=reload)
