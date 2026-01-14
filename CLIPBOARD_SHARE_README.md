# Compartir Portapapeles entre HOST y VDI

Script PowerShell para compartir texto del portapapeles entre HOST y VDI sin permisos de administrador.

## ⚠️ Limitaciones

- **Solo texto**: No funciona con archivos, imágenes, etc.
- **Requiere carpeta compartida**: Necesitas acceso a una carpeta desde ambos lados (HOST y VDI)
- **No automático**: Debes ejecutar el script manualmente

## 🚀 Uso Rápido

### Opción 1: Usar carpeta temporal (si tienes acceso)

1. **En el HOST:**
   ```powershell
   .\clipboard_share.ps1 -Mode host
   ```

2. **En la VDI:**
   ```powershell
   .\clipboard_share.ps1 -Mode vdi
   ```

### Opción 2: Usar carpeta compartida (recomendado)

1. **Crear carpeta compartida accesible desde ambos lados:**
   - Carpeta compartida en red
   - Carpeta en OneDrive/Dropbox
   - Carpeta en servidor compartido

2. **En el HOST:**
   ```powershell
   .\clipboard_share.ps1 -Mode host -SharePath "\\servidor\carpeta_compartida"
   ```

3. **En la VDI:**
   ```powershell
   .\clipboard_share.ps1 -Mode vdi -SharePath "\\servidor\carpeta_compartida"
   ```

## 📋 Modos de Uso

### Modo Manual

1. Ejecuta el script en ambos lados (HOST y VDI)
2. En el HOST: Opción 1 (Enviar texto)
3. En la VDI: Opción 2 (Recibir texto)

### Modo Automático (Monitoreo)

1. Ejecuta el script en ambos lados
2. Selecciona Opción 3 (Modo automático)
3. El script monitoreará cambios en el portapapeles y los compartirá automáticamente

## 🔧 Ejemplos

### Ejemplo 1: Carpeta compartida en red

```powershell
# En HOST
.\clipboard_share.ps1 -Mode host -SharePath "\\192.168.1.100\shared\clipboard"

# En VDI
.\clipboard_share.ps1 -Mode vdi -SharePath "\\192.168.1.100\shared\clipboard"
```

### Ejemplo 2: OneDrive/Dropbox

```powershell
# En HOST
.\clipboard_share.ps1 -Mode host -SharePath "C:\Users\TuUsuario\OneDrive\clipboard"

# En VDI
.\clipboard_share.ps1 -Mode vdi -SharePath "C:\Users\TuUsuario\OneDrive\clipboard"
```

### Ejemplo 3: Carpeta temporal (si tienes acceso desde ambos lados)

```powershell
# En HOST
.\clipboard_share.ps1 -Mode host

# En VDI (usando la misma ruta)
.\clipboard_share.ps1 -Mode vdi
```

## ⚙️ Funcionamiento

1. **HOST copia texto** → Guarda en `host_clipboard.txt`
2. **VDI lee archivo** → Copia al portapapeles de VDI
3. **VDI copia texto** → Guarda en `vdi_clipboard.txt`
4. **HOST lee archivo** → Copia al portapapeles de HOST

## 🎯 Casos de Uso

- Copiar código entre HOST y VDI
- Compartir URLs, comandos, texto
- Transferir texto rápido sin usar la app de correo

## ❌ Limitaciones

- **Solo texto**: No funciona con archivos, imágenes, etc.
- **Requiere carpeta compartida**: Necesitas acceso desde ambos lados
- **No permanente**: Debes ejecutar el script cada vez
- **Sin permisos admin**: Funciona sin permisos elevados

## 💡 Alternativa: Usar App Email

Si necesitas transferir archivos o no tienes carpeta compartida, usa la **App Email** que ya creamos:

1. Copia el texto en un archivo `.txt`
2. Usa la App Email para enviarlo
3. Descárgalo en el otro lado

## 🔒 Seguridad

- Los archivos se guardan en texto plano
- No hay cifrado
- Limpia los archivos cuando termines
- Los archivos se pueden leer desde cualquier proceso

## 📝 Notas

- El script requiere PowerShell 5.1 o superior
- No requiere permisos de administrador
- Funciona solo con texto (no archivos, imágenes, etc.)
- Debes ejecutar el script en ambos lados simultáneamente
