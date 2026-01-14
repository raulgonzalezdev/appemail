# Script simplificado para compartir portapapeles HOST <-> VDI
# Versión más simple y rápida

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("send", "receive")]
    [string]$Action = "send",
    
    [Parameter(Mandatory=$false)]
    [string]$Path = "$env:TEMP\clipboard_share"
)

# Crear directorio si no existe
if (-not (Test-Path $Path)) {
    New-Item -ItemType Directory -Path $Path -Force | Out-Null
}

$ClipboardFile = Join-Path $Path "clipboard.txt"

if ($Action -eq "send") {
    # Enviar: copiar portapapeles actual a archivo
    try {
        $clipboard = Get-Clipboard -ErrorAction SilentlyContinue
        if ($clipboard) {
            $clipboard | Out-File -FilePath $ClipboardFile -Encoding UTF8 -Force
            Write-Host "Texto copiado: $($clipboard.Length) caracteres" -ForegroundColor Green
            Write-Host "Archivo: $ClipboardFile" -ForegroundColor Yellow
        }
        else {
            Write-Host "El portapapeles está vacío" -ForegroundColor Yellow
        }
    }
    catch {
        Write-Host "Error: $_" -ForegroundColor Red
    }
}
else {
    # Recibir: leer archivo y copiar al portapapeles
    if (Test-Path $ClipboardFile) {
        try {
            $content = Get-Content -Path $ClipboardFile -Raw -Encoding UTF8
            if ($content) {
                Set-Clipboard -Value $content.Trim()
                Write-Host "Texto copiado al portapapeles: $($content.Length) caracteres" -ForegroundColor Green
            }
        }
        catch {
            Write-Host "Error: $_" -ForegroundColor Red
        }
    }
    else {
        Write-Host "No hay archivo disponible" -ForegroundColor Yellow
    }
}
