@echo off
cd /d "%~dp005_ai_examiner_agent"
"%~dp0.venv\Scripts\python.exe" -m streamlit run app.py
pause
