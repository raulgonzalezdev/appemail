# Script para recibir portapapeles en HOST desde correo
# Versión simple y rápida

param(
    [Parameter(Mandatory=$false)]
    [string]$DownloadDir = $env:TEMP
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Recibir Portapapeles desde Correo" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Siguiente paso:" -ForegroundColor Cyan
Write-Host "1. Abre App Email (app_email.py o AppEmail.exe)" -ForegroundColor White
Write-Host "2. Ve a la pestaña 'Recibir'" -ForegroundColor White
Write-Host "3. Haz clic en 'Actualizar correos'" -ForegroundColor White
Write-Host "4. Busca el correo con el archivo 'clipboard_vdi.txt'" -ForegroundColor White
Write-Host "5. Selecciona el correo" -ForegroundColor White
Write-Host "6. Haz clic en 'Descargar adjuntos del correo seleccionado'" -ForegroundColor White
Write-Host "7. Selecciona la carpeta de descarga: $DownloadDir" -ForegroundColor White
Write-Host ""
Write-Host "Después de descargar, ejecuta este script de nuevo con:" -ForegroundColor Yellow
Write-Host ".\clipboard_host_copy.ps1 -File <ruta_del_archivo_descargado>" -ForegroundColor Yellow
