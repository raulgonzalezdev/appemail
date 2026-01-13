@echo off
echo Creando ejecutable portable...
echo.

REM Verificar si pyinstaller está instalado
python -m pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstaller no está instalado. Instalando...
    pip install pyinstaller
)

echo.
echo Compilando aplicación...
pyinstaller --onefile --windowed --name "AppEmail" --add-data "credentials.json;." app_email.py

if errorlevel 1 (
    echo.
    echo ERROR: No se pudo crear el ejecutable
    pause
    exit /b 1
)

echo.
echo ========================================
echo Ejecutable creado exitosamente!
echo Ubicación: dist\AppEmail.exe
echo ========================================
echo.
echo IMPORTANTE: Copia credentials.json a la carpeta dist antes de usar el ejecutable
echo.
pause

