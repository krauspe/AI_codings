@echo off
echo Activating virtual environment and running EFE script...
call "%~dp0venv\Scripts\activate.bat"
python "%~dp0EFE_loesungen-cuda-newton.py"
pause