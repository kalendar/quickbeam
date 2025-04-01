#!/bin/bash

# Run UV sync
uv sync --extra dev

# Activate virtual environment
source .venv/bin/activate

# Check for pre-commit hook
if [ ! -f ".git/hooks/pre-commit" ]; then
    pre-commit install
fi

# Start tailwindcss in background
npx tailwindcss -i ./src/input.css -o ./static/main.css -w &

# Start FastAPI server
fastapi dev --port 5081
