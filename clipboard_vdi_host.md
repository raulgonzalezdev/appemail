# Compartir Portapapeles entre VDI (Azure) y HOST

Como la VDI está en Azure Cloud y no hay acceso directo entre HOST y VDI, la mejor solución es usar la **App Email** que ya creamos.

## 💡 Solución: Usar App Email

### Opción 1: Manual (Simple)

**En la VDI:**
1. Copia el texto que quieres compartir (Ctrl+C)
2. Abre un editor de texto (Notepad)
3. Pega el texto (Ctrl+V)
4. Guarda como archivo `.txt` (ejemplo: `clipboard.txt`)
5. Abre **App Email**
6. Ve a "Enviar" → Agrega el archivo `clipboard.txt`
7. Envía a `gq.raul@gmail.com`

**En el HOST:**
1. Abre **App Email**
2. Ve a "Recibir" → "Actualizar correos"
3. Descarga el archivo `clipboard.txt`
4. Abre el archivo y copia el texto (Ctrl+A, Ctrl+C)

### Opción 2: Script PowerShell (Más rápido)

**En la VDI:**

1. Copia el texto (Ctrl+C)
2. Ejecuta el script PowerShell:

```powershell
# Leer portapapeles y crear archivo temporal
$clipboard = Get-Clipboard
$tempFile = "$env:TEMP\clipboard.txt"
$clipboard | Out-File -FilePath $tempFile -Encoding UTF8 -Force
Write-Host "Texto guardado en: $tempFile"
Write-Host "Ahora abre App Email y envía este archivo"
```

3. Abre **App Email** y envía el archivo `$env:TEMP\clipboard.txt`

**En el HOST:**

1. Recibe el correo con **App Email**
2. Descarga el archivo
3. Ejecuta:

```powershell
# Leer archivo y copiar al portapapeles
$content = Get-Content -Path "clipboard.txt" -Raw
Set-Clipboard -Value $content.Trim()
Write-Host "Texto copiado al portapapeles"
```

## 🚀 Script Automatizado (Futuro)

Para automatizar completamente, necesitaríamos modificar `app_email.py` para agregar funciones CLI (línea de comandos) que permitan:

1. Enviar archivo directamente desde PowerShell
2. Recibir último correo y copiar al portapapeles

## 📝 Notas

- **Solo texto**: Esta solución funciona solo con texto (no imágenes, archivos, etc.)
- **Usa App Email**: Aprovecha la infraestructura que ya funciona
- **Funciona con Azure**: No requiere acceso directo entre HOST y VDI
- **Requiere ejecución manual**: Por ahora, necesitas ejecutar pasos manualmente

## ⚡ Atajo Rápido

1. **VDI:** Ctrl+C → Notepad → Guardar → App Email → Enviar
2. **HOST:** App Email → Recibir → Descargar → Abrir → Ctrl+A → Ctrl+C
