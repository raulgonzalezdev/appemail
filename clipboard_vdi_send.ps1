# Script para enviar portapapeles desde VDI usando App Email
# Versión simple y rápida

# Obtener texto del portapapeles
$clipboard = Get-Clipboard -ErrorAction SilentlyContinue

if (-not $clipboard) {
    Write-Host "El portapapeles está vacío" -ForegroundColor Yellow
    exit
}

# Crear archivo temporal
$tempDir = $env:TEMP
$tempFile = Join-Path $tempDir "clipboard_vdi.txt"
$clipboard | Out-File -FilePath $tempFile -Encoding UTF8 -Force

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Portapapeles copiado exitosamente" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Archivo creado: $tempFile" -ForegroundColor Yellow
Write-Host "Tamaño: $($clipboard.Length) caracteres" -ForegroundColor Yellow
Write-Host ""
Write-Host "Siguiente paso:" -ForegroundColor Cyan
Write-Host "1. Abre App Email (app_email.py o AppEmail.exe)" -ForegroundColor White
Write-Host "2. Ve a la pestaña 'Enviar'" -ForegroundColor White
Write-Host "3. Haz clic en 'Agregar archivo(s)'" -ForegroundColor White
Write-Host "4. Selecciona: $tempFile" -ForegroundColor White
Write-Host "5. Haz clic en 'Enviar correo'" -ForegroundColor White
Write-Host ""
Write-Host "El texto estará disponible en el HOST después de enviar." -ForegroundColor Green
