from fastapi import HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRouter
from pydantic import BaseModel

from dependencies import Session, Templates
from leaflock.tables.module import Module

router = APIRouter()


class ModuleModel(BaseModel):
    name: str
    outcomes: str
    summary: str
    textbook_id: int


@router.get("/create/module/{textbook_ident}", response_class=HTMLResponse)
def create_module_get(
    request: Request,
    textbook_ident: int,
    templates: Templates,
):
    return templates.TemplateResponse(
        request=request,
        name="create/module.html",
        context={"textbook_ident": textbook_ident},
    )


@router.post("/create/module", response_class=HTMLResponse)
def create_module_post(
    request: Request,
    module_model: ModuleModel,
    session: Session,
):
    module = Module(**module_model.model_dump())
    print(module)
    session.add(module)
    session.commit()

    return HTMLResponse(
        headers={
            "HX-Location": str(
                request.url_for("textbook_details", ident=module_model.textbook_id)
            )
        }
    )


@router.get(
    "/update/module/{module_ident}/{textbook_ident}", response_class=HTMLResponse
)
def update_module_get(
    request: Request,
    module_ident: int,
    textbook_ident: int,
    session: Session,
    templates: Templates,
):
    module = session.get(Module, ident=module_ident)

    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    return templates.TemplateResponse(
        request=request,
        name="update/module.html",
        context={
            "module": module,
            "textbook_ident": textbook_ident,
        },
    )


@router.post("/update/module/{ident}", response_class=HTMLResponse)
def update_module_post(
    request: Request,
    ident: int,
    session: Session,
    module_model: ModuleModel,
):
    module = session.get(Module, ident=ident)

    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    module.name = module_model.name
    module.outcomes = module_model.outcomes
    module.summary = module_model.summary
    module.textbook_id = module_model.textbook_id

    session.commit()

    return HTMLResponse(
        headers={
            "HX-Location": str(
                request.url_for("textbook_details", ident=module_model.textbook_id)
            )
        }
    )


@router.post("/delete/module/{ident}", response_class=HTMLResponse)
def delete_module(
    request: Request,
    ident: int,
    session: Session,
):
    module = session.get(Module, ident=ident)

    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    textbook_id = module.textbook_id

    session.delete(module)
    session.commit()

    return HTMLResponse(
        headers={
            "HX-Location": str(request.url_for("textbook_details", ident=textbook_id))
        }
    )
