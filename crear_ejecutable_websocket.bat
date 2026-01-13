@echo off
echo Creando ejecutable portable de App WebSocket...
echo.

REM Verificar si pyinstaller está instalado
python -m pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstaller no está instalado. Instalando...
    pip install pyinstaller
)

echo.
echo Compilando aplicación WebSocket...
pyinstaller --onefile --windowed --name "AppWebSocket" app_websocket.py

if errorlevel 1 (
    echo.
    echo ERROR: No se pudo crear el ejecutable
    pause
    exit /b 1
)

echo.
echo ========================================
echo Ejecutable creado exitosamente!
echo Ubicación: dist\AppWebSocket.exe
echo ========================================
echo.
echo Puedes copiar este ejecutable a tu HOST y VDI
echo.
pause

