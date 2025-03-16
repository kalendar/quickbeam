from fastapi import HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRouter
from pydantic import BaseModel
from sqlalchemy import select

from dependencies import Session, Templates
from leaflock.tables import Activity, Module

router = APIRouter()


class ActivityModel(BaseModel):
    name: str
    outcomes: str
    summary: str
    textbook_id: int
    module_ids: set[int] | int


@router.get("/create/activity/{textbook_ident}", response_class=HTMLResponse)
def create_activity_get(
    request: Request,
    textbook_ident: int,
    session: Session,
    templates: Templates,
):
    modules = session.scalars(
        select(Module).where(Module.textbook_id == textbook_ident)
    )

    return templates.TemplateResponse(
        request=request,
        name="create/activity.html",
        context={"textbook_ident": textbook_ident, "modules": modules},
    )


@router.post("/create/activity", response_class=HTMLResponse)
def create_activity_post(
    request: Request,
    activity_model: ActivityModel,
    session: Session,
):
    print(activity_model.textbook_id)
    activity = Activity(
        name=activity_model.name,
        outcomes=activity_model.outcomes,
        summary=activity_model.summary,
        textbook_id=activity_model.textbook_id,
    )

    # In the case of one selected module, it returns int not list[int]
    module_ids = (
        activity_model.module_ids
        if isinstance(activity_model.module_ids, set)
        else set([activity_model.module_ids])
    )

    activity.modules = set(
        session.scalars(select(Module).where(Module.id.in_(module_ids))).all()
    )

    session.add(activity)
    session.commit()

    return HTMLResponse(
        headers={
            "HX-Location": str(
                request.url_for("textbook_details", ident=activity_model.textbook_id)
            )
        }
    )


@router.get(
    "/update/activity/{activity_ident}/{textbook_ident}", response_class=HTMLResponse
)
def update_activity_get(
    request: Request,
    activity_ident: int,
    textbook_ident: int,
    session: Session,
    templates: Templates,
):
    activity = session.get(Activity, ident=activity_ident)

    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    modules = session.scalars(  # type:ignore
        select(Module).where(Module.textbook_id == textbook_ident)  # type:ignore
    )

    return templates.TemplateResponse(
        request=request,
        name="update/activity.html",
        context={
            "activity": activity,
            "textbook_ident": textbook_ident,
            "modules": modules,
        },
    )


@router.post("/update/activity/{ident}", response_class=HTMLResponse)
def update_activity_post(
    request: Request,
    ident: int,
    session: Session,
    activity_model: ActivityModel,
):
    activity = session.get(Activity, ident=ident)

    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    # In the case of one selected module, it returns int not list[int]
    module_ids = (
        activity_model.module_ids
        if isinstance(activity_model.module_ids, set)
        else [activity_model.module_ids]
    )

    activity.modules = set(
        session.scalars(select(Module).where(Module.id.in_(module_ids))).all()
    )

    activity.name = activity_model.name
    activity.outcomes = activity_model.outcomes
    activity.summary = activity_model.summary
    session.commit()

    return HTMLResponse(
        headers={
            "HX-Location": str(
                request.url_for("textbook_details", ident=activity.textbook_id)
            )
        }
    )


@router.post("/delete/activity/{ident}", response_class=HTMLResponse)
def delete_activity(
    request: Request,
    ident: int,
    session: Session,
):
    activity = session.get(Activity, ident=ident)

    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    textbook_id = activity.textbook_id

    session.delete(activity)
    session.commit()

    return HTMLResponse(
        headers={
            "HX-Location": str(request.url_for("textbook_details", ident=textbook_id))
        }
    )
