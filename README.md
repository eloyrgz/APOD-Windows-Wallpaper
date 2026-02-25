# APOD Windows Wallpaper
Small utility that downloads NASA's Astronomy Picture of the Day (APOD) and sets it as the Windows desktop wallpaper.

**Current status (refactor):** the code is organized as a Python package (`apod_wallpaper`) with a small CLI. Legacy CNTLM/service code, CI and several helper scripts were removed; useful unit tests are kept in the `tests` folder.

**Key files:**
- **Config:** [apod_wallpaper.conf](apod_wallpaper.conf)
- **Entrypoint:** [apod_wallpaper.py](apod_wallpaper.py)
- **Package:** [apod_wallpaper/](apod_wallpaper)
- **Tests:** [tests/](tests)

**Features**
- Downloads APOD and saves it to a local `download_path`.
- Sets the Windows wallpaper (uses pywin32 when available).
- Interactive style selection (center/stretch/fit/fill) via console.
- Config-driven (API key, URL, download path, optional proxy settings).

**Requirements**
- Windows (setting wallpaper is Windows-specific).
- Python 3.8+.
- Runtime dependencies: see [requirements.txt](requirements.txt).
- Optional: `pywin32` to actually set the wallpaper via Windows APIs.

**Install and run (recommended using `uv`)**
1. Install Python with `uv` (if you use `uv`):

```powershell
%USERPROFILE%\.local\bin\uv.exe python install 3.11 --default
%USERPROFILE%\.local\bin\uv.exe venv .venv
```

2. Activate the venv and install runtime deps:

```powershell
.venv\Scripts\activate.ps1
python -m pip install -r requirements.txt
```

3. Run the CLI (interactive):

```powershell
.venv\Scripts\python.exe -m apod_wallpaper
```

Or use the provided batch launcher:

```powershell
.\init.bat --once --verbose
```

**CLI flags**
- `--config, -c`: Path to `apod_wallpaper.conf` (default: current working directory).
- `--once`: Download and set wallpaper once, then exit.
- `--verbose, -v`: Enable INFO logging.

During interactive mode the script prints a numbered list of styles and prompts for a number (1-4) to change the wallpaper style; any other input exits.

**Testing**
- Tests are in [tests/](tests). Run them inside the venv:

```powershell
.venv\Scripts\python.exe -m unittest discover -v
```

