from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette import status

from database import create_db_and_tables
from routers import activity, module, textbook


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.mount(
    path="/static",
    app=StaticFiles(directory="static"),
    name="static",
)

app.include_router(textbook.router)
app.include_router(activity.router)
app.include_router(module.router)


@app.get("/")
def redirect(request: Request):
    return RedirectResponse(
        request.url_for("textbooks"),
        status_code=status.HTTP_302_FOUND,
    )
