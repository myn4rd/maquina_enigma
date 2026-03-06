@echo off
title Despliegue Automatizado - Maquina Enigma
color 0A


python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Python no detectado. Instalando via winget...
    winget install --id Python.Python.3.11 -e --source winget --accept-package-agreements --accept-source-agreements
    
    call RefreshEnv.cmd >nul 2>&1
) else (
    echo [+] Python ya esta instalado en el sistema.
)

echo.
echo [*] Fase 2: Configurando el Entorno de Ejecucion (Runtime)...
python -m pip install python-dotenv

echo.
echo [*] Fase 3: Ejecutando el Payload...
echo ---------------------------------------------------
python maquina.py
echo ---------------------------------------------------

pause