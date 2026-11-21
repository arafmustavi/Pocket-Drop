@echo off
setlocal
cd /d "%~dp0\.."
where py >nul 2>nul && (set PY=py) || (set PY=python)
%PY% -m venv .venv
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
pyinstaller --clean --noconfirm pocket_drop.spec
echo.
echo Built: dist\PocketDrop.exe
pause
