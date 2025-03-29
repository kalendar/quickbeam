# quickbeam
Quickbeam is a tool for authoring and managing generative textbooks, based on Open Educational Language Models.

## Installation
### Prerequisite
[`uv`](https://github.com/astral-sh/uv) for package management.

### Instructions
1. Clone this repo with `git clone https://github.com/kalendar/quickbeam.git --recurse-submodules` 
2. Initialize it with `uv sync`.
3. Set the environment variable `quickbeam_sqlite_database_path` to a valid sqlite database path. If no database file exists, it will be created. 
4. Enter the virtual environment and run `fastapi run`.

## Roadmap
- ✅ Create, update, and delete textbooks, activities, and topics.
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

## Development
### Prerequisites 
1. [`uv`](https://github.com/astral-sh/uv) for package management.
2. [`tailwindcss cli`](https://tailwindcss.com/docs/installation/tailwind-cli) for css styling.
3. [`Prettier`](https://github.com/prettier/prettier) for html/jinja/css formatting.
    1. [`prettier-plugin-tailwindcss`](https://github.com/tailwindlabs/prettier-plugin-tailwindcss) for tailwindcss class sorting.
    2. [`prettier-plugin-jinja-template`](https://github.com/davidodenwald/prettier-plugin-jinja-template) for better jinja support.
4. [`ruff`](https://github.com/astral-sh/ruff) for python linting/formatting/sorting.

It is recommended to use Visual Studio Code (VSCode), as a `.vscode` workspace settings file has been pre-configured for these tools. It is highly recommended to install these extensions to your workspace:
[Prettier](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode), 
[Ruff](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff), 
[Tailwind](https://marketplace.visualstudio.com/items?itemName=bradlc.vscode-tailwindcss),
[Better Jinja](https://marketplace.visualstudio.com/items?itemName=samuelcolvin.jinjahtml), and
[htmx-tags](https://marketplace.visualstudio.com/items?itemName=otovo-oss.htmx-tags).

### Instructions
1. Clone this repo with `git clone https://github.com/kalendar/quickbeam.git --recurse-submodules`.
2. Initialize it with `uv sync --extra dev`.
3. Set the environment variable `quickbeam_sqlite_database_path` to a valid sqlite database path. If no database file exists, it will be created. 
4. Enter the virtual environment and run `pre-commit install`, then `fastapi dev`.
5. To watch and compile CSS changes, run `npx tailwindcss -i ./src/input.css -o ./static/main.css --watch` in the root directory.

### Python Types
It is highly recommended to use a static type checker like [`pylance`](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) and to use types wherever applicable, eg. function parameters/returns, dictionaries and lists. 
