@echo off
rem Run APOD wallpaper script using the project's .venv (created via uv)
pushd %~dp0

if exist ".venv\Scripts\activate.bat" (
	call ".venv\Scripts\activate.bat"
) else (
	echo ".venv not found. Creating .venv via uv..."
	if exist "%USERPROFILE%\.local\bin\uv.exe" (
		"%USERPROFILE%\.local\bin\uv.exe" venv .venv
		if exist ".venv\Scripts\activate.bat" (
			call ".venv\Scripts\activate.bat"
		) else (
			echo Failed to create or find .venv; falling back to system Python
		)
	) else (
		echo uv not found; falling back to system Python
	)
)

rem Run the package entry point; pass through any args supplied to the batch file
python -m apod_wallpaper %*

rem Deactivate venv if activated
if defined VIRTUAL_ENV (
	call deactivate
)

popd