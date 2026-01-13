# App WebSocket Portable - Transferencia de Archivos

Aplicación portable y sencilla para transferir archivos directamente entre tu HOST y VDI usando WebSocket (sin intermediarios).

## Características

- ✅ Interfaz simple y minimalista
- ✅ Modo Servidor (HOST): recibe archivos de la VDI
- ✅ Modo Cliente (VDI): envía archivos al HOST
- ✅ Transferencia directa sin intermediarios
- ✅ Portable (no requiere instalación, solo ejecutar)
- ✅ No deja rastros permanentes en el sistema
- ✅ No requiere configuración de APIs externas

## Instalación

### 1. Instalar Dependencias

```bash
pip install websockets
```

O instalar todas las dependencias:

```bash
pip install -r requirements.txt
```

### 2. Ejecutar la Aplicación

```bash
python app_websocket.py
```

## Uso

### Configuración General

1. **En el HOST (tu computadora principal):**
   - Abre la aplicación
   - Ve a la pestaña "Configuración"
   - En "Modo Servidor", haz clic en "Iniciar Servidor"
   - Anota la IP local que aparece en la sección "Información"
   - El servidor estará escuchando en el puerto 8765 (por defecto)

2. **En la VDI (equipo virtual):**
   - Abre la aplicación
   - Ve a la pestaña "Configuración"
   - En "Modo Cliente", ingresa la IP del HOST (la que anotaste antes)
   - Ingresa el puerto (8765 por defecto)
   - Haz clic en "Conectar"

### Enviar Archivos (desde VDI a HOST)

1. En la VDI (modo Cliente):
   - Ve a la pestaña "Enviar"
   - Haz clic en "Agregar archivo(s)" y selecciona los archivos
   - Haz clic en "Enviar archivos"
   - Los archivos se enviarán al HOST y se guardarán en la carpeta `archivos_recibidos`

2. En el HOST (modo Servidor):
   - Los archivos recibidos se guardan automáticamente en la carpeta `archivos_recibidos`
   - Ve a la pestaña "Recibir" para ver los archivos recibidos

### Enviar Archivos (desde HOST a VDI)

**Nota:** Por defecto, el servidor solo recibe archivos. Para enviar desde HOST a VDI, debes:

1. En el HOST: mantener el servidor activo
2. En la VDI: conectarse como cliente
3. En el HOST: usar la pestaña "Enviar" para enviar archivos
4. Los archivos se enviarán a la VDI conectada y se guardarán en su carpeta `archivos_recibidos`

### Recibir Archivos

1. Ve a la pestaña "Recibir"
2. La lista muestra todos los archivos en la carpeta `archivos_recibidos`
3. Selecciona un archivo para ver sus detalles
4. Haz clic en "Abrir carpeta de archivos recibidos" para abrir la carpeta
5. Haz clic en "Actualizar lista" para refrescar la lista

## Ejemplo de Uso Típico

### Escenario: Transferir código desde VDI a HOST

**En el HOST:**
1. Ejecuta `app_websocket.py`
2. Ve a "Configuración" → "Iniciar Servidor"
3. Anota tu IP local (ejemplo: `192.168.1.100`)

**En la VDI:**
1. Ejecuta `app_websocket.py`
2. Ve a "Configuración" → Ingresa IP: `192.168.1.100` → Puerto: `8765` → "Conectar"
3. Ve a "Enviar" → Selecciona tus archivos de código → "Enviar archivos"

**De vuelta en el HOST:**
1. Ve a "Recibir" → Verás tus archivos en la lista
2. Haz clic en "Abrir carpeta de archivos recibidos" para acceder a ellos

## Crear Ejecutable Portable (Windows)

Para crear un ejecutable .exe portable:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "AppWebSocket" app_websocket.py
```

El ejecutable estará en la carpeta `dist/AppWebSocket.exe`

Puedes copiar este ejecutable a tu VDI y HOST para usarlo sin necesidad de instalar Python.

## Firewall y Red

### Windows Firewall

Si el firewall bloquea la conexión:

1. Abre "Windows Defender Firewall"
2. Permite la aplicación a través del firewall
3. O configura una regla para el puerto 8765 (TCP)

### Red Local

- El HOST y la VDI deben estar en la misma red local
- Si están en redes diferentes, necesitarás configuración de red adicional (VPN, tunneling, etc.)
- Verifica que no haya firewalls intermedios bloqueando el puerto

### ⚠️ IMPORTANTE: VDI en Azure Cloud

**Si tu VDI está en Azure Cloud, WebSocket NO funcionará directamente** porque:

1. **Network Security Groups (NSG)**: Azure bloquea conexiones entrantes por defecto
2. **Red Virtual (VNet)**: La VDI está en una red privada de Azure, no accesible desde Internet directamente
3. **Firewall de Azure**: Requiere configuración de reglas de firewall específicas

**Soluciones:**

**Opción 1 (Recomendada):** Usa **App Email (Gmail)** - Funciona perfectamente con Azure porque usa Internet/Gmail como intermediario.

**Opción 2:** Configurar Azure para WebSocket (complejo):
- Asignar IP pública a la VM
- Configurar NSG para permitir puerto 8765 (TCP) entrante
- Configurar reglas de firewall en la VM
- Usar la IP pública en lugar de IP local

**Opción 3:** Usar Azure Bastion o VPN para conectar las redes

## Solución de Problemas

**Error: "No se pudo conectar"**
- Verifica que el servidor esté ejecutándose en el HOST
- Verifica que la IP y puerto sean correctos
- Verifica que ambos equipos estén en la misma red
- Verifica que el firewall no esté bloqueando la conexión

**Error: "Puerto ya en uso"**
- Cambia el puerto en la configuración del servidor
- Cierra otras aplicaciones que puedan estar usando el puerto

**Los archivos no se reciben**
- Verifica que el servidor esté activo
- Verifica que la conexión esté establecida (modo cliente debe mostrar "Conectado")
- Revisa la carpeta `archivos_recibidos` directamente

**No puedo ver la IP local**
- La aplicación intenta detectar automáticamente la IP
- Si no se muestra, puedes obtenerla manualmente:
  - Windows: `ipconfig` en CMD (busca "IPv4 Address")
  - Linux/Mac: `ifconfig` o `ip addr`

## Seguridad

- Los archivos se transfieren sin cifrado (texto plano)
- Solo funciona en redes locales (no expuesto a Internet por defecto)
- No hay autenticación (cualquiera en tu red puede conectarse si conoce la IP)
- Para uso en redes compartidas, considera usar una VPN o configuración de firewall más estricta

## Comparación con App Email

| Característica | App Email | App WebSocket |
|----------------|-----------|---------------|
| Requiere configuración | Sí (Google Cloud) | No |
| Requiere Internet | Sí | No (solo red local) |
| Velocidad | Limitada por Gmail | Rápida (red local) |
| Límite de tamaño | ~25MB (Gmail) | Sin límite práctico |
| Privacidad | Archivos en Gmail | Transferencia directa |
| Portabilidad | Alta | Alta |

**Recomendación:** 
- Usa **App WebSocket** si estás en la misma red local (más rápido y simple)
- Usa **App Email** si necesitas transferir archivos a través de Internet o redes separadas

