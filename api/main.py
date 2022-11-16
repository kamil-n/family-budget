import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from api.config import ApiSettings
from api.db import Base, engine
from api.routers import budget, token, user

Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(user.router, tags=["Users"])
app.include_router(budget.router, tags=["Budgets"])
app.include_router(token.router, tags=["Token"])

settings = ApiSettings()


@app.get("/", include_in_schema=False)
async def docs_redirect() -> RedirectResponse:
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    reload = settings.env == "dev"
    uvicorn.run("main:app", host=settings.ap_host, port=settings.ap_port, reload=reload)
