@echo off
cd /d "%~dp004_llm_basic_app"
"%~dp0.venv\Scripts\python.exe" -m streamlit run app.py
pause
