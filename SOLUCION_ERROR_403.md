# Solución Error 403: Gmail API no habilitada

## 🔴 Error que estás viendo

```
Error 403: Gmail API has not been used in project 860981657786 before or it is disabled.
```

Este error significa que la **API de Gmail no está habilitada** en tu proyecto de Google Cloud.

## ✅ Solución Rápida

### Paso 1: Habilitar la API de Gmail

1. **Ve directamente a este enlace:**
   https://console.developers.google.com/apis/api/gmail.googleapis.com/overview?project=860981657786

   O sigue estos pasos:

2. **Ve a Google Cloud Console:**
   https://console.cloud.google.com/

3. **Asegúrate de tener seleccionado el proyecto correcto:**
   - En la parte superior, verifica que el proyecto sea: **business-one-395214** (project ID: 860981657786)
   - Si no es el correcto, haz clic en el selector de proyectos y selecciona el correcto

4. **Habilita la API de Gmail:**
   - En el menú lateral izquierdo, ve a **"APIs y servicios"** → **"Biblioteca"**
   - O ve directamente a: https://console.cloud.google.com/apis/library
   - En la barra de búsqueda, escribe: **"Gmail API"**
   - Selecciona **"Gmail API"** de los resultados
   - Haz clic en el botón **"HABILITAR"** (aparece en azul)
   - Espera unos segundos hasta que se habilite

### Paso 2: Esperar unos minutos (si acabas de habilitar)

- Si acabas de habilitar la API, **espera 2-5 minutos**
- Google necesita tiempo para propagar los cambios a sus sistemas

### Paso 3: Intentar de nuevo

1. Cierra la aplicación si está abierta
2. Vuelve a ejecutar: `python app_email.py`
3. Intenta enviar el correo nuevamente

## 🔍 Verificar que la API esté habilitada

1. Ve a: https://console.cloud.google.com/apis/library
2. Busca "Gmail API"
3. Si está habilitada, verás un botón **"ADMINISTRAR"** (en lugar de "HABILITAR")
4. También puedes verificar en: https://console.cloud.google.com/apis/dashboard

## ❌ Si el error persiste

### Verifica el proyecto

1. Ve a: https://console.cloud.google.com/
2. Asegúrate de estar en el proyecto correcto: **business-one-395214**
3. Si creaste las credenciales en otro proyecto, necesitas usar ese proyecto o recrear las credenciales

### Verifica las credenciales

1. Verifica que `credentials.json` esté en la misma carpeta que `app_email.py`
2. Verifica que el archivo tenga el formato correcto (debe tener `"installed"`, no `"web"`)

### Error de permisos

Si el error persiste después de habilitar la API y esperar unos minutos:

1. Elimina el archivo `token.pickle` (si existe)
2. Vuelve a ejecutar la aplicación
3. Vuelve a autenticarte cuando se abra el navegador

## 📝 Notas Importantes

- ✅ **La API de Gmail es gratuita** para uso personal
- ✅ **No necesitas pagar nada** para habilitarla
- ⏱️ **Espera 2-5 minutos** después de habilitar la API antes de intentar de nuevo
- 🔑 **Asegúrate de estar en el proyecto correcto** (business-one-395214)

