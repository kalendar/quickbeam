from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from leaflock.database import create_database
from starlette import status

from routers import activity, textbook, topic
from settings import SETTINGS


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_database(database_path=SETTINGS.sqlite_database_path)
    yield


app = FastAPI(lifespan=lifespan)

app.mount(
    path="/static",
    app=StaticFiles(directory="static"),
    name="static",
)

app.include_router(textbook.router)
app.include_router(activity.router)
app.include_router(topic.router)


@app.get("/")
def redirect(request: Request):
    return RedirectResponse(
        request.url_for("textbooks"),
        status_code=status.HTTP_302_FOUND,
    )
