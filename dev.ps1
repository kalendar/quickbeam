# Run UV sync
uv sync --extra dev

# Activate virtual environment
.\.venv\Scripts\activate

# Check for pre-commit hook
if (-not (Test-Path -Path ".git\hooks\pre-commit")) {
    pre-commit install
}

# Start tailwindcss at correct version, can't use same terminal because fastapi dev kills it on reload.
Start-Process -FilePath "powershell" -ArgumentList "npm ci; npx tailwindcss -i .\src\input.css -o .\static\main.css -w"

# Start FastAPI server
fastapi dev --port 5081
