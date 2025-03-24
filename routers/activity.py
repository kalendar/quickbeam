import uuid
from typing import Optional

from fastapi import HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRouter
from leaflock.sqlalchemy_tables.activity import Activity
from leaflock.sqlalchemy_tables.module import Module
from pydantic import BaseModel
from sqlalchemy import select

from dependencies import Session, Templates

router = APIRouter()


class ActivityModel(BaseModel):
    name: str
    description: str
    prompt: str
    textbook_guid: uuid.UUID
    module_guids: Optional[set[uuid.UUID] | uuid.UUID] = None


@router.get("/create/activity/{textbook_ident}", response_class=HTMLResponse)
def create_activity_get(
    request: Request,
    textbook_ident: uuid.UUID,
    session: Session,
    templates: Templates,
):
    modules = session.scalars(
        select(Module).where(Module.textbook_guid == textbook_ident)
    )

    return templates.TemplateResponse(
        request=request,
        name="create/activity.jinja",
        context={"textbook_ident": textbook_ident, "modules": modules},
    )


@router.post("/create/activity", response_class=HTMLResponse)
def create_activity_post(
    request: Request,
    activity_model: ActivityModel,
    session: Session,
):
    activity = Activity(
        name=activity_model.name,
        description=activity_model.description,
        prompt=activity_model.prompt,
    )

    activity.textbook_guid = activity_model.textbook_guid

    # In the case of one selected module, it returns int not list[int]
    module_ids = (
        activity_model.module_guids
        if isinstance(activity_model.module_guids, set)
        else set([activity_model.module_guids])
    )

    activity.modules = set(
        session.scalars(select(Module).where(Module.guid.in_(module_ids))).all()
    )

    session.add(activity)
    session.commit()

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
    session: Session,
    templates: Templates,
):
    activity = session.get(Activity, ident=activity_ident)

    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    modules = session.scalars(  # type:ignore
        select(Module).where(Module.textbook_guid == textbook_ident)  # type:ignore
    )

    return templates.TemplateResponse(
        request=request,
        name="update/activity.jinja",
        context={
            "activity": activity,
            "textbook_ident": textbook_ident,
            "modules": modules,
        },
    )


@router.post("/update/activity/{ident}", response_class=HTMLResponse)
def update_activity_post(
    request: Request,
    ident: uuid.UUID,
    session: Session,
    activity_model: ActivityModel,
):
    activity = session.get(Activity, ident=ident)

    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    # In the case of one selected module, it returns uuid.UUID not list[uuid.UUID]
    module_guids = (
        activity_model.module_guids
        if isinstance(activity_model.module_guids, set)
        else [activity_model.module_guids]
    )

    activity.modules = set(
        session.scalars(select(Module).where(Module.guid.in_(module_guids))).all()
    )

    activity.name = activity_model.name
    activity.description = activity_model.description
    activity.prompt = activity_model.prompt
    session.commit()

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
    session: Session,
):
    activity = session.get(Activity, ident=ident)

    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    textbook_guid = activity.textbook_guid

    session.delete(activity)
    session.commit()

    return HTMLResponse(
        headers={
            "HX-Location": str(request.url_for("textbook_details", ident=textbook_guid))
        }
    )
