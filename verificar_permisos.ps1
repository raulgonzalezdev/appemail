# Script para verificar permisos de administrador
# Ejecuta este script para verificar si tienes permisos suficientes

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Verificación de Permisos" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar si el usuario actual es administrador
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if ($isAdmin) {
    Write-Host "Estado: Tienes permisos de ADMINISTRADOR" -ForegroundColor Green
    Write-Host ""
    Write-Host "Puedes intentar habilitar el portapapeles compartido RDP." -ForegroundColor Yellow
}
else {
    Write-Host "Estado: NO tienes permisos de administrador" -ForegroundColor Red
    Write-Host ""
    Write-Host "No puedes:" -ForegroundColor Yellow
    Write-Host "- Cambiar el registro del sistema" -ForegroundColor White
    Write-Host "- Crear usuarios con permisos de administrador" -ForegroundColor White
    Write-Host "- Habilitar portapapeles compartido RDP" -ForegroundColor White
    Write-Host "- Modificar políticas de grupo" -ForegroundColor White
    Write-Host ""
    Write-Host "Solución recomendada: Usar App Email" -ForegroundColor Green
}

Write-Host ""
Write-Host "Información del Usuario:" -ForegroundColor Cyan
Write-Host "Usuario: $env:USERNAME" -ForegroundColor White
Write-Host "Computadora: $env:COMPUTERNAME" -ForegroundColor White
Write-Host ""

# Ver grupos de usuario
Write-Host "Grupos del usuario:" -ForegroundColor Cyan
whoami /groups | Select-String -Pattern "BUILTIN|Domain" | ForEach-Object {
    Write-Host "  $_" -ForegroundColor White
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
