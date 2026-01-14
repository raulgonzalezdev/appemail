# Script para enviar portapapeles de VDI a HOST usando App Email
# Requiere que app_email.py esté configurado y funcionando

param(
    [Parameter(Mandatory=$false)]
    [string]$Email = "gq.raul@gmail.com"
)

# Obtener texto del portapapeles
try {
    $clipboard = Get-Clipboard -ErrorAction SilentlyContinue
    if (-not $clipboard) {
        Write-Host "El portapapeles está vacío" -ForegroundColor Yellow
        exit 1
    }
    
    # Crear archivo temporal
    $tempFile = Join-Path $env:TEMP "clipboard_$(Get-Date -Format 'yyyyMMdd_HHmmss').txt"
    $clipboard | Out-File -FilePath $tempFile -Encoding UTF8 -Force
    
    Write-Host "Texto copiado del portapapeles: $($clipboard.Length) caracteres" -ForegroundColor Green
    Write-Host "Archivo temporal: $tempFile" -ForegroundColor Yellow
    
    # Intentar enviar usando Python directamente (si app_email.py tiene función CLI)
    # Por ahora, mostrar instrucciones
    Write-Host ""
    Write-Host "Para enviar:" -ForegroundColor Cyan
    Write-Host "1. Abre App Email (app_email.py)" -ForegroundColor White
    Write-Host "2. Ve a la pestaña 'Enviar'" -ForegroundColor White
    Write-Host "3. Agrega el archivo: $tempFile" -ForegroundColor White
    Write-Host "4. Envía el correo a: $Email" -ForegroundColor White
    Write-Host ""
    Write-Host "O usa Python directamente:" -ForegroundColor Cyan
    Write-Host "python -c `"from app_email import *; import sys; sys.path.insert(0, '.'); exec(open('app_email.py').read().split('if __name__')[0] + 'app = EmailApp(None); app.send_clipboard_file(\"$tempFile\", \"$Email\");')`""
    
}
catch {
    Write-Host "Error: $_" -ForegroundColor Red
    exit 1
}
