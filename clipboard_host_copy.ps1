# Script para copiar contenido de archivo al portapapeles en HOST

param(
    [Parameter(Mandatory=$true)]
    [string]$File
)

if (-not (Test-Path $File)) {
    Write-Host "Error: El archivo no existe: $File" -ForegroundColor Red
    exit 1
}

try {
    $content = Get-Content -Path $File -Raw -Encoding UTF8
    if ($content) {
        Set-Clipboard -Value $content.Trim()
        Write-Host "========================================" -ForegroundColor Cyan
        Write-Host "Texto copiado al portapapeles" -ForegroundColor Green
        Write-Host "========================================" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "Archivo: $File" -ForegroundColor Yellow
        Write-Host "Tamaño: $($content.Length) caracteres" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Puedes pegar ahora (Ctrl+V)" -ForegroundColor Green
    }
    else {
        Write-Host "El archivo está vacío" -ForegroundColor Yellow
    }
}
catch {
    Write-Host "Error al leer archivo: $_" -ForegroundColor Red
    exit 1
}
