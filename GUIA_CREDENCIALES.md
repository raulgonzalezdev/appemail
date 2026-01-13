# Guía Paso a Paso: Obtener Credenciales de Google Cloud

Guía simplificada para configurar las credenciales OAuth 2.0 necesarias para la App Email con cuenta Gmail personal.

## 📋 Requisitos Previos

- Una cuenta de Gmail personal (@gmail.com)
- Acceso a Internet
- Un navegador web

## 🚀 Paso a Paso

### Paso 1: Crear un Proyecto en Google Cloud Console

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Si es la primera vez, acepta los términos y condiciones
3. Haz clic en el **selector de proyectos** (arriba a la izquierda, junto a "Google Cloud")
4. Haz clic en **"NUEVO PROYECTO"**
5. Ingresa un nombre para el proyecto (ejemplo: `App Email Portable`)
6. Haz clic en **"CREAR"**
7. Espera unos segundos hasta que el proyecto se cree

### Paso 2: Habilitar la API de Gmail

1. En el menú lateral izquierdo, busca **"APIs y servicios"** → **"Biblioteca"**
   - O ve directamente a: https://console.cloud.google.com/apis/library
2. En la barra de búsqueda, escribe: **"Gmail API"**
3. Selecciona **"Gmail API"** de los resultados
4. Haz clic en el botón **"HABILITAR"** (aparece en azul)
5. Espera unos segundos hasta que se habilite

### Paso 3: Configurar la Pantalla de Consentimiento OAuth

1. En el menú lateral izquierdo, ve a **"APIs y servicios"** → **"Pantalla de consentimiento OAuth"**
   - O ve directamente a: https://console.cloud.google.com/apis/credentials/consent
2. Selecciona **"Externo"** y haz clic en **"CREAR"**
3. Completa el formulario:
   - **Nombre de la aplicación**: `App Email Portable` (o el que prefieras)
   - **Correo electrónico de soporte del usuario**: Tu correo (ejemplo: `gq.raul@gmail.com`)
   - **Correo electrónico de contacto del desarrollador**: Tu correo
4. Haz clic en **"GUARDAR Y CONTINUAR"**
5. En **"Ámbitos"**, haz clic en **"GUARDAR Y CONTINUAR"** (sin cambios)
6. En **"Usuarios de prueba"**, haz clic en **"GUARDAR Y CONTINUAR"** (opcional, puedes agregar tu correo como usuario de prueba)
7. En **"Resumen"**, revisa la información y haz clic en **"VOLVER AL PANEL"**

### Paso 4: Crear las Credenciales OAuth 2.0

1. En el menú lateral izquierdo, ve a **"APIs y servicios"** → **"Credenciales"**
   - O ve directamente a: https://console.cloud.google.com/apis/credentials
2. Haz clic en **"+ CREAR CREDENCIALES"** (arriba)
3. Selecciona **"ID de cliente de OAuth"**
4. Si te pide configurar la pantalla de consentimiento primero, sigue el Paso 3
5. En la ventana "Crear ID de cliente de OAuth":
   - **Tipo de aplicación**: Selecciona **"Aplicación de escritorio"** (Desktop app)
   - **Nombre**: `App Email Portable` (o el que prefieras)
6. Haz clic en **"CREAR"**
7. Se mostrará una ventana con las credenciales
   - **⚠️ IMPORTANTE**: No cierres esta ventana todavía

### Paso 5: Descargar las Credenciales

1. En la ventana de credenciales creadas:
   - Haz clic en el botón **"DESCARGAR JSON"** (arriba a la derecha)
   - O haz clic en **"OK"** y luego en el icono de descarga junto a tu credencial
2. Se descargará un archivo JSON (ejemplo: `client_secret_xxxxx.json`)
3. **Renombra este archivo** a: `credentials.json`
4. **Mueve este archivo** a la misma carpeta donde está `app_email.py`

### Paso 6: Verificar la Ubicación del Archivo

Tu estructura de archivos debería verse así:

```
appemail/
├── app_email.py
├── credentials.json          ← Este archivo debe estar aquí
├── requirements.txt
└── ...
```

## ✅ Verificación

1. Verifica que `credentials.json` esté en la misma carpeta que `app_email.py`
2. Verifica que el archivo se llame exactamente `credentials.json` (sin espacios adicionales)
3. Ejecuta la aplicación:
   ```bash
   python app_email.py
   ```

4. La primera vez que ejecutes la app:
   - Se abrirá una ventana del navegador
   - Te pedirá iniciar sesión con tu cuenta de Google
   - Te pedirá permisos para acceder a Gmail
   - Acepta los permisos
   - Se creará automáticamente un archivo `token.pickle` (este guarda tu sesión)

## 🔒 Seguridad

- **NO compartas** el archivo `credentials.json` con nadie
- **NO subas** `credentials.json` a repositorios públicos (GitHub, etc.)
- El archivo `token.pickle` también contiene información sensible
- Si alguien tiene estos archivos, puede acceder a tu Gmail

## ❌ Solución de Problemas

### Error: "No se encuentra credentials.json"
- Verifica que el archivo esté en la misma carpeta que `app_email.py`
- Verifica que el nombre sea exactamente `credentials.json` (sin espacios)

### Error: "Error 403: access_denied"
- Verifica que hayas habilitado la API de Gmail (Paso 2)
- Verifica que hayas configurado la pantalla de consentimiento (Paso 3)
- Intenta eliminar `token.pickle` y vuelve a ejecutar la app

### Error: "redirect_uri_mismatch"
- Asegúrate de haber seleccionado "Aplicación de escritorio" en el Paso 4
- Verifica que el tipo de credencial sea "Desktop app"

### La ventana del navegador no se abre
- Verifica que tu firewall no esté bloqueando la aplicación
- Intenta ejecutar la app desde la línea de comandos para ver los errores

### "Este tipo de cliente de OAuth no está autorizado"
- Espera unos minutos después de crear las credenciales
- Verifica que hayas seleccionado "Aplicación de escritorio" (Desktop app)
- Intenta crear las credenciales nuevamente

## 📝 Notas Importantes

- ✅ **Funciona con cuenta Gmail personal gratuita** (@gmail.com)
- ✅ **No necesitas pagar nada** - Google Cloud tiene cuota gratuita generosa
- ✅ **Solo selecciona "Externo"** en la pantalla de consentimiento (Paso 3)
- ✅ **Gmail API es gratuita** para uso personal
