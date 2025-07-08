@echo off
REM Cambia esta ruta a donde tienes tu proyecto
cd /d C:\Users\Germancho\Desktop\crm_link

REM Activa el entorno virtual
call venv\Scripts\activate

REM Ejecuta FastAPI con uvicorn
uvicorn main:app --reload

pause
