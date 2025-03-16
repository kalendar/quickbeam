from typing import Annotated

import jinjax
from fastapi import Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session as SQLASession

from database import get_session

__TEMPLATES = Jinja2Templates(directory="templates")

__TEMPLATES.env.add_extension(jinjax.JinjaX)  # type: ignore
__TEMPLATES.env.globals["len"] = len  # type:ignore
__CATALOG = jinjax.Catalog(jinja_env=__TEMPLATES.env)  # type: ignore
__CATALOG.add_folder("templates/components")


def get_templates() -> Jinja2Templates:
    return __TEMPLATES


Templates = Annotated[Jinja2Templates, Depends(get_templates)]
Session = Annotated[SQLASession, Depends(get_session)]
