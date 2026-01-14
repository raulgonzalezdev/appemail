# Uso Rápido del Script de Portapapeles Simple

## Versión Simple (Recomendada)

Script más simple con dos comandos: `send` y `receive`

### Uso Básico

1. **En HOST (después de copiar texto):**
   ```powershell
   .\clipboard_share_simple.ps1 -Action send
   ```

2. **En VDI (para recibir):**
   ```powershell
   .\clipboard_share_simple.ps1 -Action receive
   ```

### Con Carpeta Compartida

Si tienes una carpeta compartida accesible desde ambos lados:

1. **En HOST:**
   ```powershell
   .\clipboard_share_simple.ps1 -Action send -Path "\\servidor\carpeta\clipboard"
   ```

2. **En VDI:**
   ```powershell
   .\clipboard_share_simple.ps1 -Action receive -Path "\\servidor\carpeta\clipboard"
   ```

### Atajos Rápidos

Crea alias en PowerShell:

```powershell
# En el HOST
Set-Alias -Name csend -Value ".\clipboard_share_simple.ps1 -Action send"

# En la VDI
Set-Alias -Name crecv -Value ".\clipboard_share_simple.ps1 -Action receive"
```

Luego solo usa:
- `csend` para enviar
- `crecv` para recibir

## Ejemplo de Flujo

1. **En HOST:**
   - Copias código/texto (Ctrl+C)
   - Ejecutas: `.\clipboard_share_simple.ps1 -Action send`

2. **En VDI:**
   - Ejecutas: `.\clipboard_share_simple.ps1 -Action receive`
   - Pegas el texto (Ctrl+V)

## Requisitos

- PowerShell 5.1 o superior
- Acceso a carpeta compartida (o usar carpeta temporal si es accesible desde ambos lados)
- Sin permisos de administrador
