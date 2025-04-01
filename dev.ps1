# Run UV sync
uv sync --extra dev

# Activate virtual environment
.\.venv\Scripts\activate

# Check for pre-commit hook
if (-not (Test-Path -Path ".git\hooks\pre-commit")) {
    pre-commit install
}

# Start tailwindcss in background
Start-Process -NoNewWindow -FilePath "cmd" -ArgumentList "/c npx tailwindcss -i .\src\input.css -o .\static\main.css -w"

# Start FastAPI server
fastapi dev --port 5081
