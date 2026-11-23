@echo off
chcp 65001 >nul
cd /d "%~dp0"
if exist ".venv\Scripts\python.exe" (set PY=.venv\Scripts\python.exe) else (set PY=py -3.12)
echo Встановлюю huggingface_hub...
%PY% -m pip install --quiet --upgrade huggingface_hub
%PY% deploy_to_hf.py
echo.
pause
