import uuid
from typing import Optional

from fastapi import HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRouter
from pydantic import BaseModel
from sqlalchemy import select

from dependencies import ReadSession, Templates, WriteSession
from leaflock.sqlalchemy_tables.activity import Activity
from leaflock.sqlalchemy_tables.topic import Topic

router = APIRouter()


class ActivityModel(BaseModel):
    name: str

    description: str
    prompt: str

    sources: str
    authors: str

    textbook_guid: uuid.UUID
    topic_guids: Optional[set[uuid.UUID] | uuid.UUID] = None


@router.get("/create/activity/{textbook_ident}", response_class=HTMLResponse)
def create_activity_get(
    request: Request,
    textbook_ident: uuid.UUID,
    session: ReadSession,
    templates: Templates,
):
    topics = session.scalars(select(Topic).where(Topic.textbook_guid == textbook_ident))

    return templates.TemplateResponse(
        request=request,
        name="create/activity.jinja",
        context={"textbook_ident": textbook_ident, "topics": topics},
    )


@router.post("/create/activity", response_class=HTMLResponse)
def create_activity_post(
    request: Request,
    activity_model: ActivityModel,
    session: WriteSession,
):
    activity = Activity(
        name=activity_model.name,
        description=activity_model.description,
        prompt=activity_model.prompt,
        authors=activity_model.authors,
        sources=activity_model.sources,
    )

    activity.textbook_guid = activity_model.textbook_guid

    # In the case of one selected topic, it returns int not list[int]
    topic_guids = (
        activity_model.topic_guids
        if isinstance(activity_model.topic_guids, set)
        else set([activity_model.topic_guids])
    )

    activity.topics = set(
        session.scalars(select(Topic).where(Topic.guid.in_(topic_guids))).all()
    )

    session.add(activity)

    return HTMLResponse(
        headers={
            "HX-Location": str(
                request.url_for("textbook_details", ident=activity_model.textbook_guid)
            )
        }
    )


@router.get(
    "/update/activity/{activity_ident}/{textbook_ident}", response_class=HTMLResponse
)
def update_activity_get(
    request: Request,
    activity_ident: uuid.UUID,
    textbook_ident: uuid.UUID,
    session: ReadSession,
    templates: Templates,
):
    activity = session.get(Activity, ident=activity_ident)

    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    topics = session.scalars(  # type:ignore
        select(Topic).where(Topic.textbook_guid == textbook_ident)  # type:ignore
    )

    return templates.TemplateResponse(
        request=request,
        name="update/activity.jinja",
        context={
            "activity": activity,
            "textbook_ident": textbook_ident,
            "topics": topics,
        },
    )


@router.post("/update/activity/{ident}", response_class=HTMLResponse)
def update_activity_post(
    request: Request,
    ident: uuid.UUID,
    session: WriteSession,
    activity_model: ActivityModel,
):
    activity = session.get(Activity, ident=ident)

    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    # In the case of one selected topic, it returns uuid.UUID not list[uuid.UUID]
    topic_guids = (
        activity_model.topic_guids
        if isinstance(activity_model.topic_guids, set)
        else [activity_model.topic_guids]
    )

    activity.topics = set(
        session.scalars(select(Topic).where(Topic.guid.in_(topic_guids))).all()
    )

    activity.name = activity_model.name
    activity.description = activity_model.description
    activity.prompt = activity_model.prompt
    activity.authors = activity_model.authors
    activity.sources = activity_model.sources

    # Ensure dirty
    session.add(activity)

    return HTMLResponse(
        headers={
            "HX-Location": str(
                request.url_for("textbook_details", ident=activity.textbook_guid)
            )
        }
    )


@router.post("/delete/activity/{ident}", response_class=HTMLResponse)
def delete_activity(
    request: Request,
    ident: uuid.UUID,
    session: WriteSession,
):
    activity = session.get(Activity, ident=ident)

    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    textbook_guid = activity.textbook_guid

    session.delete(activity)

    return HTMLResponse(
        headers={
            "HX-Location": str(request.url_for("textbook_details", ident=textbook_guid))
        }
    )
