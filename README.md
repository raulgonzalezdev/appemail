# App Transfer - Transferencia de Archivos

Aplicaciones portables y sencillas para transferir archivos entre tu HOST y VDI.

Este repositorio contiene **dos aplicaciones** para transferir archivos:

## 📧 App Email (Gmail) ⭐ RECOMENDADA PARA AZURE

Transferencia de archivos usando Gmail como intermediario. **Funciona perfectamente con VDI en Azure Cloud** sin necesidad de configurar redes o firewalls.

**Archivo:** `app_email.py`

**✅ Ideal para:**
- VDI en Azure Cloud, AWS, o cualquier cloud
- HOST y VDI en redes diferentes
- Sin acceso a configuración de red

Ver: [README Email](README.md) (instrucciones en el código principal)

## 🔌 App WebSocket

Transferencia directa de archivos usando WebSocket. Más rápido y simple, **solo funciona si HOST y VDI están en la misma red local**.

**Archivo:** `app_websocket.py`

**⚠️ NO funciona con Azure Cloud sin configuración compleja** (ver [AZURE_NOTAS.md](AZURE_NOTAS.md))

**✅ Ideal para:**
- HOST y VDI en la misma red local
- Máxima velocidad de transferencia
- Sin límites de tamaño

Ver: [README WebSocket](README_WEBSOCKET.md)

## ¿Cuál usar?

| Escenario | Recomendación |
|-----------|---------------|
| HOST y VDI en la misma red local | **App WebSocket** (más rápido) |
| HOST y VDI en redes diferentes | **App Email** (funciona vía Internet) |
| VDI en Azure Cloud / AWS / Cloud | **App Email** (funciona sin configuración) |
| Necesitas transferir sin configurar red | **App Email** (usa Gmail) |
| Quieres máxima velocidad (misma red) | **App WebSocket** (transfers directos) |

## Instalación Rápida

### Para App Email

```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
python app_email.py
```

### Para App WebSocket

```bash
pip install websockets
python app_websocket.py
```

### Para Ambas

```bash
pip install -r requirements.txt
```

## Crear Ejecutables Portables

### App Email

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "AppEmail" app_email.py
```

O ejecuta: `crear_ejecutable.bat`

### App WebSocket

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "AppWebSocket" app_websocket.py
```

O ejecuta: `crear_ejecutable_websocket.bat`

## Características Comunes

- ✅ Portables (pueden compilarse a .exe)
- ✅ Interfaz simple y minimalista
- ✅ No dejan rastros permanentes en el sistema
- ✅ Funcionales y fáciles de usar

## Uso Rápido

### App WebSocket (Recomendado para redes locales)

**En el HOST:**
1. Ejecuta `app_websocket.py`
2. Ve a "Configuración" → "Iniciar Servidor"
3. Anota tu IP local

**En la VDI:**
1. Ejecuta `app_websocket.py`
2. Ve a "Configuración" → Ingresa IP del HOST → "Conectar"
3. Ve a "Enviar" → Selecciona archivos → "Enviar archivos"

**Ver archivos recibidos:** Pestaña "Recibir" → "Abrir carpeta de archivos recibidos"

### App Email (Para redes separadas)

**Configuración inicial (una vez):**
1. Configura Google Cloud Console (ver instrucciones en `app_email.py`)
2. Descarga `credentials.json`

**Enviar archivos:**
1. Ejecuta `app_email.py`
2. Ve a "Enviar" → Selecciona archivos → "Enviar correo"

**Recibir archivos:**
1. Ve a "Recibir" → "Actualizar correos"
2. Selecciona un correo → "Descargar adjuntos"

## Solución de Problemas

### App WebSocket

- **Error de conexión:** Verifica que ambos equipos estén en la misma red
- **Firewall:** Permite el puerto 8765 (TCP) en Windows Firewall
- **IP no detectada:** Obtén la IP manualmente con `ipconfig` (Windows)

### App Email

- **Error de credenciales:** Verifica que `credentials.json` esté en la misma carpeta
- **Error de autenticación:** Elimina `token.pickle` y vuelve a autenticarte
- **No aparecen correos:** Verifica que los correos tengan adjuntos

## Archivos del Proyecto

```
appemail/
├── app_email.py              # App Email (Gmail) ⭐ Para Azure
├── app_websocket.py          # App WebSocket (Directo)
├── requirements.txt          # Dependencias
├── README.md                 # Este archivo
├── README_WEBSOCKET.md       # Documentación App WebSocket
├── AZURE_NOTAS.md            # Notas específicas para Azure Cloud
├── crear_ejecutable.bat      # Script para crear .exe de Email
└── crear_ejecutable_websocket.bat  # Script para crear .exe de WebSocket
```

## ⚠️ VDI en Azure Cloud?

**Si tu VDI está en Azure Cloud, usa App Email (Gmail).** 

WebSocket no funcionará sin configuración compleja de Azure (NSG, IP pública, firewall). 

Ver detalles en: [AZURE_NOTAS.md](AZURE_NOTAS.md)

## Licencia

Uso libre para propósitos personales y educativos.
