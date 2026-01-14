# Script para compartir portapapeles entre HOST y VDI
# No requiere permisos de administrador
# Usa archivos temporales en una carpeta compartida o accesible desde ambos lados

param(
    [Parameter(Mandatory=$false)]
    [string]$Mode = "host",  # "host" o "vdi"
    
    [Parameter(Mandatory=$false)]
    [string]$SharePath = ""  # Ruta compartida (opcional)
)

# Carpeta temporal para intercambio
$TempDir = $env:TEMP
$ClipboardDir = Join-Path $TempDir "clipboard_share"

# Si se especifica una ruta compartida, usarla
if ($SharePath -ne "") {
    $ClipboardDir = $SharePath
}

# Crear directorio si no existe
if (-not (Test-Path $ClipboardDir)) {
    New-Item -ItemType Directory -Path $ClipboardDir -Force | Out-Null
}

$HostFile = Join-Path $ClipboardDir "host_clipboard.txt"
$VdiFile = Join-Path $ClipboardDir "vdi_clipboard.txt"
$LockFile = Join-Path $ClipboardDir "clipboard.lock"

function Write-HostClipboard {
    # Lee el portapapeles del HOST y lo guarda en archivo
    try {
        $clipboard = Get-Clipboard -ErrorAction SilentlyContinue
        if ($clipboard) {
            $clipboard | Out-File -FilePath $HostFile -Encoding UTF8 -Force
            Write-Host "Texto copiado desde HOST: $($clipboard.Length) caracteres" -ForegroundColor Green
            return $true
        }
    }
    catch {
        Write-Host "Error al leer portapapeles: $_" -ForegroundColor Red
    }
    return $false
}

function Read-HostClipboard {
    # Lee el archivo del HOST y lo copia al portapapeles de la VDI
    if (Test-Path $HostFile) {
        try {
            $content = Get-Content -Path $HostFile -Raw -Encoding UTF8
            if ($content) {
                Set-Clipboard -Value $content.Trim()
                Write-Host "Texto copiado a portapapeles de VDI: $($content.Length) caracteres" -ForegroundColor Green
                return $true
            }
        }
        catch {
            Write-Host "Error al leer archivo: $_" -ForegroundColor Red
        }
    }
    return $false
}

function Write-VdiClipboard {
    # Lee el portapapeles de la VDI y lo guarda en archivo
    try {
        $clipboard = Get-Clipboard -ErrorAction SilentlyContinue
        if ($clipboard) {
            $clipboard | Out-File -FilePath $VdiFile -Encoding UTF8 -Force
            Write-Host "Texto copiado desde VDI: $($clipboard.Length) caracteres" -ForegroundColor Green
            return $true
        }
    }
    catch {
        Write-Host "Error al leer portapapeles: $_" -ForegroundColor Red
    }
    return $false
}

function Read-VdiClipboard {
    # Lee el archivo de la VDI y lo copia al portapapeles del HOST
    if (Test-Path $VdiFile) {
        try {
            $content = Get-Content -Path $VdiFile -Raw -Encoding UTF8
            if ($content) {
                Set-Clipboard -Value $content.Trim()
                Write-Host "Texto copiado a portapapeles de HOST: $($content.Length) caracteres" -ForegroundColor Green
                return $true
            }
        }
        catch {
            Write-Host "Error al leer archivo: $_" -ForegroundColor Red
        }
    }
    return $false
}

# Menú interactivo
function Show-Menu {
    Clear-Host
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "  Compartir Portapapeles HOST <-> VDI" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Modo: $Mode" -ForegroundColor Yellow
    Write-Host "Carpeta: $ClipboardDir" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Opciones:" -ForegroundColor White
    Write-Host "  1. Enviar texto al otro lado (Copiar desde aquí)"
    Write-Host "  2. Recibir texto del otro lado (Pegar desde allí)"
    Write-Host "  3. Modo automático (monitoreo continuo)"
    Write-Host "  4. Cambiar modo (host/vdi)"
    Write-Host "  5. Cambiar carpeta compartida"
    Write-Host "  0. Salir"
    Write-Host ""
}

function Start-AutoMode {
    Write-Host ""
    Write-Host "Modo automático activado. Presiona Ctrl+C para salir." -ForegroundColor Yellow
    Write-Host "Monitoreando cambios en el portapapeles..." -ForegroundColor Yellow
    Write-Host ""
    
    $lastHash = ""
    
    while ($true) {
        try {
            if ($Mode -eq "host") {
                $clipboard = Get-Clipboard -ErrorAction SilentlyContinue
                if ($clipboard) {
                    $currentHash = $clipboard | ConvertTo-Json | Get-FileHash -Algorithm MD5
                    if ($currentHash.Hash -ne $lastHash) {
                        $lastHash = $currentHash.Hash
                        Write-HostClipboard
                    }
                }
            }
            else {
                $clipboard = Get-Clipboard -ErrorAction SilentlyContinue
                if ($clipboard) {
                    $currentHash = $clipboard | ConvertTo-Json | Get-FileHash -Algorithm MD5
                    if ($currentHash.Hash -ne $lastHash) {
                        $lastHash = $currentHash.Hash
                        Write-VdiClipboard
                    }
                }
            }
            
            Start-Sleep -Milliseconds 500
        }
        catch {
            Start-Sleep -Seconds 1
        }
    }
}

# Bucle principal
while ($true) {
    Show-Menu
    $choice = Read-Host "Selecciona una opción"
    
    switch ($choice) {
        "1" {
            if ($Mode -eq "host") {
                Write-HostClipboard
            }
            else {
                Write-VdiClipboard
            }
            Write-Host ""
            Read-Host "Presiona Enter para continuar"
        }
        "2" {
            if ($Mode -eq "host") {
                Read-VdiClipboard
            }
            else {
                Read-HostClipboard
            }
            Write-Host ""
            Read-Host "Presiona Enter para continuar"
        }
        "3" {
            Start-AutoMode
        }
        "4" {
            $newMode = Read-Host "Ingresa modo (host/vdi)"
            if ($newMode -eq "host" -or $newMode -eq "vdi") {
                $Mode = $newMode
            }
        }
        "5" {
            $newPath = Read-Host "Ingresa ruta completa de carpeta compartida (Enter para usar temp)"
            if ($newPath -ne "") {
                $ClipboardDir = $newPath
                if (-not (Test-Path $ClipboardDir)) {
                    New-Item -ItemType Directory -Path $ClipboardDir -Force | Out-Null
                }
                $HostFile = Join-Path $ClipboardDir "host_clipboard.txt"
                $VdiFile = Join-Path $ClipboardDir "vdi_clipboard.txt"
            }
        }
        "0" {
            Write-Host "Saliendo..." -ForegroundColor Yellow
            exit
        }
        default {
            Write-Host "Opción inválida" -ForegroundColor Red
            Start-Sleep -Seconds 1
        }
    }
}
