# quickbeam
OELM authoring and management.

## Installation or Development
Clone this repo with `git clone https://github.com/kalendar/quickbeam.git --recurse-submodules` and initialize it with `uv sync`.

Set the environment variable `quickbeam_sqlite_database_path` to a valid database path. If no database file exists, it will be created. 

Enter the virtual environment and run `fastapi run` for installation, or `fastapi dev` for development.

## Roadmap
- ✅ Create, update, and delete textbooks, activities, and modules.
- ⬜ Export/Import textbooks.
- ⬜ Organize textbooks.

## Repo Organization
- `/leaflock` - OELM Textbook definition.
- `/routers` - Routers for individual elements, creation/update/deletion.
- `/src` - Tailwindcss css source file.
- `/static` - Static files.
- `/templates`
    - template files, organized by purpose (eg /get, /create, /update).
    - `/components` - JinjaX components.
- `database.py` - Create the database based on leaflock definitions.
- `dependencies.py` - Template and Session dependencies for FastAPI.
- `main.py` - FastAPI entry point.
- `settings.py` - Pydantic settings definition.
