from fastapi import HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRouter
from leaflock.sqlalchemy_tables import Textbook
from pydantic import BaseModel
from sqlalchemy import select

from dependencies import Session, Templates

router = APIRouter()


class TextbookModel(BaseModel):
    title: str
    prompt: str
    authors: str


@router.get("/textbooks", response_class=HTMLResponse)
def textbooks(
    request: Request,
    session: Session,
    templates: Templates,
):
    textbooks = session.scalars(select(Textbook)).all()

    return templates.TemplateResponse(
        request=request,
        name="textbooks.jinja",
        context={"textbooks": textbooks},
    )


@router.get("/get/textbook/{ident}", response_class=HTMLResponse)
def textbook_details(
    request: Request,
    ident: int,
    session: Session,
    templates: Templates,
):
    textbook = session.get(Textbook, ident=ident)

    return templates.TemplateResponse(
        request=request,
        name="get/textbook.jinja",
        context={"textbook": textbook},
    )


@router.get("/create/textbook", response_class=HTMLResponse)
def create_textbook_get(
    request: Request,
    templates: Templates,
):
    return templates.TemplateResponse(
        request=request,
        name="create/textbook.jinja",
    )


@router.post("/create/textbook", response_class=HTMLResponse)
def create_textbook_post(
    request: Request,
    textbook_model: TextbookModel,
    session: Session,
):
    session.add(Textbook(**textbook_model.model_dump()))
    session.commit()

    return HTMLResponse(headers={"HX-Location": str(request.url_for("textbooks"))})


@router.get("/update/textbook/{ident}", response_class=HTMLResponse)
def update_textbook_get(
    request: Request,
    ident: int,
    session: Session,
    templates: Templates,
):
    textbook = session.get(Textbook, ident=ident)

    return templates.TemplateResponse(
        request=request,
        name="update/textbook.jinja",
        context={"textbook": textbook},
    )


@router.post("/update/textbook/{ident}", response_class=HTMLResponse)
def update_textbook_post(
    request: Request,
    ident: int,
    session: Session,
    textbook_model: TextbookModel,
):
    textbook = session.get(Textbook, ident=ident)

    if not textbook:
        raise HTTPException(status_code=404, detail="Textbook not found")

    textbook.title = textbook_model.title
    textbook.prompt = textbook_model.prompt
    textbook.authors = textbook_model.authors

    session.commit()

    return HTMLResponse(
        headers={"HX-Location": str(request.url_for("textbook_details", ident=ident))}
    )


@router.post("/delete/textbook/{ident}", response_class=HTMLResponse)
def delete_textbook(
    request: Request,
    ident: int,
    session: Session,
):
    textbook = session.get(Textbook, ident=ident)

    if not textbook:
        raise HTTPException(status_code=404, detail="Textbook not found")

    session.delete(textbook)
    session.commit()

    return HTMLResponse(headers={"HX-Location": str(request.url_for("textbooks"))})
