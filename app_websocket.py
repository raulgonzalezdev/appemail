#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
App WebSocket Portable - Transferencia de archivos vía WebSocket
Aplicación simple para transferir archivos entre host y VDI
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import asyncio
import websockets
import json
import base64
import os
import threading
from datetime import datetime
import socket

try:
    import websockets
except ImportError:
    messagebox.showerror("Error", "Por favor instala las dependencias:\npip install websockets")
    exit(1)

DEFAULT_PORT = 8765
RECEIVED_FILES_DIR = "archivos_recibidos"


class WebSocketApp:
    def __init__(self, root):
        self.root = root
        self.root.title("App WebSocket - Transferencia de Archivos")
        self.root.geometry("700x600")
        self.root.resizable(False, False)
        
        # Estado
        self.mode = None  # 'server' o 'client'
        self.server = None
        self.server_thread = None
        self.server_loop = None
        self.websocket = None
        self.client_loop = None
        self.connected = False
        self.server_running = False
        self.client_connections = set()  # Conexiones de clientes en modo servidor
        
        # Crear directorio para archivos recibidos
        if not os.path.exists(RECEIVED_FILES_DIR):
            os.makedirs(RECEIVED_FILES_DIR)
        
        # Interfaz
        self.create_ui()
    
    def create_ui(self):
        """Crea la interfaz de usuario"""
        # Notebook para pestañas
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Pestaña de Configuración
        config_frame = ttk.Frame(notebook)
        notebook.add(config_frame, text="Configuración")
        self.create_config_tab(config_frame)
        
        # Pestaña de Envío
        send_frame = ttk.Frame(notebook)
        notebook.add(send_frame, text="Enviar")
        self.create_send_tab(send_frame)
        
        # Pestaña de Recepción
        receive_frame = ttk.Frame(notebook)
        notebook.add(receive_frame, text="Recibir")
        self.create_receive_tab(receive_frame)
        
        # Status bar
        self.status_var = tk.StringVar(value="Desconectado - Selecciona modo Servidor o Cliente")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def create_config_tab(self, parent):
        """Crea la pestaña de configuración"""
        # Frame para modo Servidor
        server_frame = ttk.LabelFrame(parent, text="Modo Servidor (HOST)")
        server_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(server_frame, text="El servidor escucha conexiones entrantes.\nÚsalo en tu HOST para recibir archivos de la VDI.").pack(padx=5, pady=5)
        
        port_frame = ttk.Frame(server_frame)
        port_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(port_frame, text="Puerto:").pack(side=tk.LEFT, padx=5)
        self.server_port_entry = ttk.Entry(port_frame, width=10)
        self.server_port_entry.insert(0, str(DEFAULT_PORT))
        self.server_port_entry.pack(side=tk.LEFT, padx=5)
        
        self.server_start_btn = ttk.Button(server_frame, text="Iniciar Servidor", command=self.start_server)
        self.server_start_btn.pack(pady=5)
        
        self.server_stop_btn = ttk.Button(server_frame, text="Detener Servidor", command=self.stop_server, state=tk.DISABLED)
        self.server_stop_btn.pack(pady=5)
        
        # Frame para modo Cliente
        client_frame = ttk.LabelFrame(parent, text="Modo Cliente (VDI)")
        client_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(client_frame, text="El cliente se conecta al servidor.\nÚsalo en tu VDI para enviar archivos al HOST.").pack(padx=5, pady=5)
        
        connect_frame = ttk.Frame(client_frame)
        connect_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(connect_frame, text="IP del Host:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.client_ip_entry = ttk.Entry(connect_frame, width=20)
        self.client_ip_entry.grid(row=0, column=1, padx=5, pady=5)
        self.client_ip_entry.insert(0, "localhost")
        
        ttk.Label(connect_frame, text="Puerto:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.client_port_entry = ttk.Entry(connect_frame, width=10)
        self.client_port_entry.insert(0, str(DEFAULT_PORT))
        self.client_port_entry.grid(row=0, column=3, padx=5, pady=5)
        
        self.client_connect_btn = ttk.Button(client_frame, text="Conectar", command=self.connect_client)
        self.client_connect_btn.pack(pady=5)
        
        self.client_disconnect_btn = ttk.Button(client_frame, text="Desconectar", command=self.disconnect_client, state=tk.DISABLED)
        self.client_disconnect_btn.pack(pady=5)
        
        # Información de IP
        info_frame = ttk.LabelFrame(parent, text="Información")
        info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.ip_info_text = tk.Text(info_frame, height=4, wrap=tk.WORD)
        self.ip_info_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.update_ip_info()
    
    def create_send_tab(self, parent):
        """Crea la pestaña de envío"""
        ttk.Label(parent, text="Archivos a enviar:").pack(anchor=tk.W, padx=5, pady=5)
        
        file_frame = ttk.Frame(parent)
        file_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.file_listbox = tk.Listbox(file_frame, height=10)
        scrollbar = ttk.Scrollbar(file_frame, orient=tk.VERTICAL, command=self.file_listbox.yview)
        self.file_listbox.config(yscrollcommand=scrollbar.set)
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.selected_files = []
        
        # Botones de archivos
        file_buttons = ttk.Frame(parent)
        file_buttons.pack(pady=5)
        
        ttk.Button(file_buttons, text="Agregar archivo(s)", command=self.add_files).pack(side=tk.LEFT, padx=2)
        ttk.Button(file_buttons, text="Quitar seleccionado", command=self.remove_file).pack(side=tk.LEFT, padx=2)
        
        # Botón enviar
        self.send_btn = ttk.Button(parent, text="Enviar archivos", command=self.send_files, state=tk.DISABLED)
        self.send_btn.pack(pady=10)
    
    def create_receive_tab(self, parent):
        """Crea la pestaña de recepción"""
        ttk.Label(parent, text="Archivos recibidos:").pack(anchor=tk.W, padx=5, pady=5)
        
        list_frame = ttk.Frame(parent)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.received_listbox = tk.Listbox(list_frame, height=10)
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.received_listbox.yview)
        self.received_listbox.config(yscrollcommand=scrollbar.set)
        self.received_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Info de archivo
        info_frame = ttk.LabelFrame(parent, text="Detalles")
        info_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.file_info_text = scrolledtext.ScrolledText(info_frame, height=4, wrap=tk.WORD)
        self.file_info_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Botones
        button_frame = ttk.Frame(parent)
        button_frame.pack(pady=5)
        
        ttk.Button(button_frame, text="Abrir carpeta de archivos recibidos", 
                  command=self.open_received_folder).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="Actualizar lista", 
                  command=self.refresh_received_files).pack(side=tk.LEFT, padx=2)
        
        self.received_files = []
        self.refresh_received_files()
    
    def update_ip_info(self):
        """Actualiza la información de IP"""
        try:
            # Obtener IP local
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
        except:
            local_ip = "No disponible"
        
        info_text = f"Tu IP local: {local_ip}\n"
        info_text += f"Puerto por defecto: {DEFAULT_PORT}\n"
        info_text += f"En el cliente (VDI), usa esta IP para conectarte al servidor (HOST)"
        
        self.ip_info_text.delete(1.0, tk.END)
        self.ip_info_text.insert(1.0, info_text)
    
    def start_server(self):
        """Inicia el servidor WebSocket"""
        try:
            port = int(self.server_port_entry.get())
            if port < 1 or port > 65535:
                raise ValueError("Puerto inválido")
        except ValueError:
            messagebox.showerror("Error", "Puerto inválido. Debe ser un número entre 1 y 65535.")
            return
        
        def run_server():
            async def server_handler(websocket, path):
                try:
                    self.client_connections.add(websocket)
                    self.root.after(0, lambda: self.status_var.set(f"Cliente conectado: {websocket.remote_address}"))
                    await self.handle_client(websocket)
                except websockets.exceptions.ConnectionClosed:
                    self.client_connections.discard(websocket)
                    self.root.after(0, lambda: self.status_var.set("Cliente desconectado"))
                except Exception as e:
                    self.client_connections.discard(websocket)
                    self.root.after(0, lambda: self.log_error(f"Error en cliente: {str(e)}"))
                finally:
                    self.client_connections.discard(websocket)
            
            async def start_ws_server():
                self.server = await websockets.serve(server_handler, "0.0.0.0", port)
                self.root.after(0, lambda: self.server_start_btn.config(state=tk.DISABLED))
                self.root.after(0, lambda: self.server_stop_btn.config(state=tk.NORMAL))
                self.root.after(0, lambda: self.status_var.set(f"Servidor escuchando en puerto {port}"))
                await asyncio.Future()  # Ejecutar indefinidamente
            
            self.server_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.server_loop)
            self.server_loop.run_until_complete(start_ws_server())
        
        self.server_thread = threading.Thread(target=run_server, daemon=True)
        self.server_thread.start()
        
        self.server_running = True
        self.send_btn.config(state=tk.NORMAL)
    
    def stop_server(self):
        """Detiene el servidor WebSocket"""
        if self.server:
            async def close_server():
                self.server.close()
                await self.server.wait_closed()
            
            if self.server_loop and self.server_loop.is_running():
                asyncio.run_coroutine_threadsafe(close_server(), self.server_loop)
        
        self.server_running = False
        self.client_connections.clear()
        self.server_start_btn.config(state=tk.NORMAL)
        self.server_stop_btn.config(state=tk.DISABLED)
        self.send_btn.config(state=tk.DISABLED)
        self.status_var.set("Servidor detenido")
    
    def connect_client(self):
        """Conecta el cliente al servidor"""
        ip = self.client_ip_entry.get().strip()
        try:
            port = int(self.client_port_entry.get())
            if port < 1 or port > 65535:
                raise ValueError("Puerto inválido")
        except ValueError:
            messagebox.showerror("Error", "Puerto inválido.")
            return
        
        if not ip:
            messagebox.showerror("Error", "Ingresa la IP del servidor.")
            return
        
        def connect_thread():
            async def connect():
                try:
                    uri = f"ws://{ip}:{port}"
                    self.websocket = await websockets.connect(uri)
                    self.connected = True
                    self.root.after(0, lambda: self.status_var.set(f"Conectado a {ip}:{port}"))
                    self.root.after(0, lambda: self.client_connect_btn.config(state=tk.DISABLED))
                    self.root.after(0, lambda: self.client_disconnect_btn.config(state=tk.NORMAL))
                    self.root.after(0, lambda: self.send_btn.config(state=tk.NORMAL))
                    
                    # Mantener conexión y escuchar mensajes
                    await self.handle_server_messages()
                except Exception as e:
                    self.connected = False
                    self.root.after(0, lambda: self.status_var.set(f"Error de conexión: {str(e)}"))
                    self.root.after(0, lambda: messagebox.showerror("Error", f"No se pudo conectar: {str(e)}"))
                    self.root.after(0, lambda: self.client_connect_btn.config(state=tk.NORMAL))
                    self.root.after(0, lambda: self.client_disconnect_btn.config(state=tk.DISABLED))
                    self.root.after(0, lambda: self.send_btn.config(state=tk.DISABLED))
            
            self.client_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.client_loop)
            self.client_loop.run_until_complete(connect())
        
        threading.Thread(target=connect_thread, daemon=True).start()
    
    def disconnect_client(self):
        """Desconecta el cliente"""
        if self.websocket and self.client_loop:
            async def close():
                await self.websocket.close()
            asyncio.run_coroutine_threadsafe(close(), self.client_loop)
        self.connected = False
        self.client_connect_btn.config(state=tk.NORMAL)
        self.client_disconnect_btn.config(state=tk.DISABLED)
        self.send_btn.config(state=tk.DISABLED)
        self.status_var.set("Desconectado")
    
    async def handle_client(self, websocket):
        """Maneja las conexiones de clientes (en modo servidor)"""
        async for message in websocket:
            try:
                data = json.loads(message)
                if data['type'] == 'file':
                    await self.receive_file(websocket, data)
                elif data['type'] == 'message':
                    self.root.after(0, lambda msg=data['message']: self.status_var.set(f"Mensaje: {msg}"))
            except json.JSONDecodeError:
                pass
            except Exception as e:
                self.root.after(0, lambda: self.log_error(f"Error procesando mensaje: {str(e)}"))
    
    async def handle_server_messages(self):
        """Maneja mensajes del servidor (en modo cliente)"""
        try:
            async for message in self.websocket:
                try:
                    data = json.loads(message)
                    if data['type'] == 'file':
                        await self.receive_file(self.websocket, data)
                    elif data['type'] == 'ack':
                        pass  # Confirmación recibida
                except json.JSONDecodeError:
                    pass
        except websockets.exceptions.ConnectionClosed:
            self.connected = False
            self.root.after(0, lambda: self.status_var.set("Conexión cerrada"))
            self.root.after(0, lambda: self.client_connect_btn.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.client_disconnect_btn.config(state=tk.DISABLED))
            self.root.after(0, lambda: self.send_btn.config(state=tk.DISABLED))
    
    async def receive_file(self, websocket, data):
        """Recibe un archivo"""
        filename = data['filename']
        file_data = base64.b64decode(data['data'])
        file_size = len(file_data)
        
        # Guardar archivo
        file_path = os.path.join(RECEIVED_FILES_DIR, filename)
        
        # Evitar sobrescribir
        counter = 1
        base_name, ext = os.path.splitext(filename)
        while os.path.exists(file_path):
            file_path = os.path.join(RECEIVED_FILES_DIR, f"{base_name}_{counter}{ext}")
            counter += 1
        
        with open(file_path, 'wb') as f:
            f.write(file_data)
        
        self.root.after(0, lambda: self.status_var.set(f"Archivo recibido: {os.path.basename(file_path)}"))
        self.root.after(0, lambda: self.refresh_received_files())
        self.root.after(0, lambda: messagebox.showinfo("Archivo recibido", 
            f"Archivo guardado:\n{os.path.basename(file_path)}\n\nTamaño: {file_size} bytes"))
        
        # Enviar confirmación (solo si hay websocket)
        if websocket:
            try:
                response = {'type': 'ack', 'message': 'Archivo recibido correctamente'}
                await websocket.send(json.dumps(response))
            except Exception:
                pass  # Ignorar errores de confirmación
    
    def add_files(self):
        """Agrega archivos a la lista"""
        files = filedialog.askopenfilenames(title="Seleccionar archivos")
        for file in files:
            if file not in self.selected_files:
                self.selected_files.append(file)
                self.file_listbox.insert(tk.END, os.path.basename(file))
    
    def remove_file(self):
        """Remueve el archivo seleccionado"""
        selection = self.file_listbox.curselection()
        if selection:
            index = selection[0]
            self.file_listbox.delete(index)
            del self.selected_files[index]
    
    def send_files(self):
        """Envía los archivos seleccionados"""
        if not self.selected_files:
            messagebox.showwarning("Advertencia", "No hay archivos seleccionados.")
            return
        
        if not self.connected and not self.server_running:
            messagebox.showerror("Error", "No hay conexión activa. Conéctate como cliente o inicia el servidor.")
            return
        
        def send_thread():
            async def send():
                for file_path in self.selected_files:
                    try:
                        filename = os.path.basename(file_path)
                        
                        with open(file_path, 'rb') as f:
                            file_data = f.read()
                        
                        # Codificar archivo en base64
                        encoded_data = base64.b64encode(file_data).decode('utf-8')
                        
                        # Crear mensaje
                        message = {
                            'type': 'file',
                            'filename': filename,
                            'data': encoded_data,
                            'size': len(file_data)
                        }
                        
                        if self.connected and self.websocket and self.client_loop:
                            # Modo cliente: enviar al servidor
                            await self.websocket.send(json.dumps(message))
                            self.root.after(0, lambda fn=filename: self.status_var.set(f"Enviando: {fn}"))
                            # Esperar confirmación
                            try:
                                response = await asyncio.wait_for(self.websocket.recv(), timeout=5.0)
                            except asyncio.TimeoutError:
                                pass
                        elif self.server_running and self.client_connections:
                            # Modo servidor: enviar a todos los clientes conectados
                            message_str = json.dumps(message)
                            disconnected = set()
                            for client in self.client_connections:
                                try:
                                    await client.send(message_str)
                                    self.root.after(0, lambda fn=filename: self.status_var.set(f"Enviando: {fn}"))
                                except Exception:
                                    disconnected.add(client)
                            # Limpiar conexiones desconectadas
                            self.client_connections -= disconnected
                        else:
                            self.root.after(0, lambda: messagebox.showerror("Error", "No hay conexión disponible."))
                            return
                        
                        await asyncio.sleep(0.1)
                        
                    except Exception as e:
                        self.root.after(0, lambda fn=filename, err=str(e): messagebox.showerror("Error", f"Error al enviar {fn}: {err}"))
                
                self.root.after(0, lambda: self.status_var.set("Archivos enviados"))
                self.root.after(0, lambda: messagebox.showinfo("Éxito", "Archivos enviados correctamente"))
                self.root.after(0, lambda: self.file_listbox.delete(0, tk.END))
                self.root.after(0, lambda: setattr(self, 'selected_files', []))
            
            if self.connected and self.client_loop:
                asyncio.run_coroutine_threadsafe(send(), self.client_loop)
            elif self.server_running and self.server_loop:
                asyncio.run_coroutine_threadsafe(send(), self.server_loop)
            else:
                messagebox.showerror("Error", "No hay conexión activa.")
        
        threading.Thread(target=send_thread, daemon=True).start()
    
    def refresh_received_files(self):
        """Actualiza la lista de archivos recibidos"""
        self.received_listbox.delete(0, tk.END)
        self.received_files = []
        
        if os.path.exists(RECEIVED_FILES_DIR):
            files = os.listdir(RECEIVED_FILES_DIR)
            for file in sorted(files, key=lambda x: os.path.getmtime(os.path.join(RECEIVED_FILES_DIR, x)), reverse=True):
                file_path = os.path.join(RECEIVED_FILES_DIR, file)
                if os.path.isfile(file_path):
                    size = os.path.getsize(file_path)
                    mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
                    display_name = f"{file} ({self.format_size(size)}) - {mtime.strftime('%Y-%m-%d %H:%M')}"
                    self.received_listbox.insert(tk.END, display_name)
                    self.received_files.append(file_path)
            
            # Bind para mostrar info
            self.received_listbox.bind('<<ListboxSelect>>', self.show_file_info)
    
    def show_file_info(self, event):
        """Muestra información del archivo seleccionado"""
        selection = self.received_listbox.curselection()
        if selection:
            index = selection[0]
            file_path = self.received_files[index]
            info = f"Archivo: {os.path.basename(file_path)}\n"
            info += f"Tamaño: {self.format_size(os.path.getsize(file_path))}\n"
            info += f"Ubicación: {os.path.abspath(file_path)}"
            self.file_info_text.delete(1.0, tk.END)
            self.file_info_text.insert(1.0, info)
    
    def open_received_folder(self):
        """Abre la carpeta de archivos recibidos"""
        folder_path = os.path.abspath(RECEIVED_FILES_DIR)
        os.startfile(folder_path) if os.name == 'nt' else os.system(f'xdg-open "{folder_path}"')
    
    def format_size(self, size):
        """Formatea el tamaño del archivo"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"
    
    def log_error(self, message):
        """Registra un error"""
        self.status_var.set(f"Error: {message}")
        print(f"Error: {message}")


def main():
    root = tk.Tk()
    app = WebSocketApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()

