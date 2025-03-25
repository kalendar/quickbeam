import uuid

from fastapi import HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRouter
from leaflock.sqlalchemy_tables.topic import Topic
from pydantic import BaseModel

from dependencies import Session, Templates

router = APIRouter()


class TopicModel(BaseModel):
    name: str
    outcomes: str
    summary: str
    textbook_guid: uuid.UUID


@router.get("/create/topic/{textbook_ident}", response_class=HTMLResponse)
def create_topic_get(
    request: Request,
    textbook_ident: uuid.UUID,
    templates: Templates,
):
    return templates.TemplateResponse(
        request=request,
        name="create/topic.jinja",
        context={"textbook_ident": textbook_ident},
    )


@router.post("/create/topic", response_class=HTMLResponse)
def create_topic_post(
    request: Request,
    topic_model: TopicModel,
    session: Session,
):
    topic = Topic(
        name=topic_model.name,
        outcomes=topic_model.outcomes,
        summary=topic_model.summary,
    )

    topic.textbook_guid = topic_model.textbook_guid

    session.add(topic)
    session.commit()

    return HTMLResponse(
        headers={
            "HX-Location": str(
                request.url_for("textbook_details", ident=topic_model.textbook_guid)
            )
        }
    )


@router.get(
    "/update/topic/{topic_ident}/{textbook_ident}", response_class=HTMLResponse
)
def update_topic_get(
    request: Request,
    topic_ident: uuid.UUID,
    textbook_ident: uuid.UUID,
    session: Session,
    templates: Templates,
):
    topic = session.get(Topic, ident=topic_ident)

    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    return templates.TemplateResponse(
        request=request,
        name="update/topic.jinja",
        context={
            "topic": topic,
            "textbook_ident": textbook_ident,
        },
    )


@router.post("/update/topic/{ident}", response_class=HTMLResponse)
def update_topic_post(
    request: Request,
    ident: uuid.UUID,
    session: Session,
    topic_model: TopicModel,
):
    topic = session.get(Topic, ident=ident)

    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    topic.name = topic_model.name
    topic.outcomes = topic_model.outcomes
    topic.summary = topic_model.summary
    topic.textbook_guid = topic_model.textbook_guid

    session.commit()

    return HTMLResponse(
        headers={
            "HX-Location": str(
                request.url_for("textbook_details", ident=topic_model.textbook_guid)
            )
        }
    )


@router.post("/delete/topic/{ident}", response_class=HTMLResponse)
def delete_topic(
    request: Request,
    ident: uuid.UUID,
    session: Session,
):
    topic = session.get(Topic, ident=ident)

    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    textbook_guid = topic.textbook_guid

    session.delete(topic)
    session.commit()

    return HTMLResponse(
        headers={
            "HX-Location": str(request.url_for("textbook_details", ident=textbook_guid))
        }
    )
