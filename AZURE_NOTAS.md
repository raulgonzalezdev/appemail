# Notas para VDI en Azure Cloud

## ⚠️ Problema con WebSocket en Azure

Si tu VDI está en **Azure Cloud**, la aplicación WebSocket **NO funcionará directamente** sin configuración adicional compleja.

### ¿Por qué no funciona?

1. **Network Security Groups (NSG)**: Azure bloquea todas las conexiones entrantes por defecto
2. **Red Virtual Privada**: La VDI está en una VNet privada, no accesible desde Internet
3. **Firewall de Azure**: Requiere reglas específicas para permitir conexiones

### ✅ Solución Recomendada: App Email (Gmail)

**Usa `app_email.py` en lugar de `app_websocket.py`**

La App Email funciona perfectamente con Azure porque:
- ✅ Usa Gmail como intermediario (funciona a través de Internet)
- ✅ No requiere configuración de red en Azure
- ✅ No necesita abrir puertos ni configurar NSG
- ✅ Funciona desde cualquier lugar (HOST y VDI pueden estar en cualquier red)

### Cómo usar App Email con Azure VDI

1. **Configuración inicial (una vez):**
   - Configura Google Cloud Console
   - Descarga `credentials.json`
   - Colócalo en la misma carpeta que `app_email.py`

2. **En tu HOST:**
   - Ejecuta `app_email.py`
   - Ve a "Enviar" → Selecciona archivos → "Enviar correo"
   - Los archivos se envían a `gq.raul@gmail.com`

3. **En la VDI de Azure:**
   - Ejecuta `app_email.py`
   - Ve a "Recibir" → "Actualizar correos"
   - Selecciona el correo → "Descargar adjuntos"

### Alternativa: Configurar Azure para WebSocket (No recomendado)

Si realmente quieres usar WebSocket, necesitarías:

1. **Asignar IP pública a la VM:**
   ```bash
   # En Azure Portal o Azure CLI
   az network public-ip create --name myPublicIP --resource-group myResourceGroup
   az network nic ip-config update --name ipconfig1 --nic-name myVMNic --resource-group myResourceGroup --public-ip myPublicIP
   ```

2. **Configurar NSG para permitir puerto 8765:**
   ```bash
   az network nsg rule create \
     --resource-group myResourceGroup \
     --nsg-name myNSG \
     --name AllowWebSocket \
     --priority 1000 \
     --protocol Tcp \
     --destination-port-ranges 8765 \
     --access Allow
   ```

3. **Configurar firewall en la VM:**
   - Windows: Permitir puerto 8765 en Windows Firewall
   - Linux: Configurar iptables o firewalld

4. **Usar IP pública en lugar de IP local:**
   - En el cliente, usar la IP pública de Azure en lugar de IP local

**Problemas de esta solución:**
- ❌ Expone tu VM a Internet (riesgo de seguridad)
- ❌ Requiere conocimientos de Azure
- ❌ Más complejo de mantener
- ❌ Puede violar políticas de seguridad corporativas

### Recomendación Final

**Para VDI en Azure Cloud, usa App Email (Gmail).** Es más simple, seguro y funciona sin configuración adicional.

