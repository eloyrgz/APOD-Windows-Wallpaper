<#
Run tests inside the project's .venv. Creates .venv if missing.
Usage: .\run-tests.ps1
#>
if (-not (Test-Path ".venv")) {
    Write-Output "Virtual env not found. Creating .venv via uv..."
    & "$env:USERPROFILE\.local\bin\uv.exe" venv .venv
}

& .\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pip install -r requirements-dev.txt
python -m unittest discover -v
