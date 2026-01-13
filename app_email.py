#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
App Email Portable - Transferencia de archivos vía Gmail
Aplicación simple para enviar y recibir archivos adjuntos por correo
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import base64
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import pickle
import threading

try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError:
    messagebox.showerror("Error", "Por favor instala las dependencias:\npip install -r requirements.txt")
    exit(1)

SCOPES = ['https://www.googleapis.com/auth/gmail.send', 'https://www.googleapis.com/auth/gmail.readonly']
TOKEN_FILE = 'token.pickle'
CREDENTIALS_FILE = 'credentials.json'
DEFAULT_EMAIL = 'gq.raul@gmail.com'


class EmailApp:
    def __init__(self, root):
        self.root = root
        self.root.title("App Email Portable")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Servicio de Gmail
        self.service = None
        
        # Interfaz
        self.create_ui()
        
        # Intentar cargar credenciales
        self.load_credentials()
    
    def create_ui(self):
        """Crea la interfaz de usuario"""
        # Notebook para pestañas
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Pestaña de Envío
        send_frame = ttk.Frame(notebook)
        notebook.add(send_frame, text="Enviar")
        self.create_send_tab(send_frame)
        
        # Pestaña de Recepción
        receive_frame = ttk.Frame(notebook)
        notebook.add(receive_frame, text="Recibir")
        self.create_receive_tab(receive_frame)
        
        # Status bar
        self.status_var = tk.StringVar(value="Listo")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def create_send_tab(self, parent):
        """Crea la pestaña de envío"""
        # Destinatario
        ttk.Label(parent, text="Para:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.to_entry = ttk.Entry(parent, width=50)
        self.to_entry.insert(0, DEFAULT_EMAIL)
        self.to_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Asunto
        ttk.Label(parent, text="Asunto:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.subject_entry = ttk.Entry(parent, width=50)
        self.subject_entry.insert(0, "Transferencia de archivo")
        self.subject_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Archivos seleccionados
        ttk.Label(parent, text="Archivos:").grid(row=2, column=0, sticky=tk.NW, padx=5, pady=5)
        file_frame = ttk.Frame(parent)
        file_frame.grid(row=2, column=1, sticky=tk.EW, padx=5, pady=5)
        
        self.file_listbox = tk.Listbox(file_frame, height=8, width=50)
        scrollbar = ttk.Scrollbar(file_frame, orient=tk.VERTICAL, command=self.file_listbox.yview)
        self.file_listbox.config(yscrollcommand=scrollbar.set)
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.selected_files = []
        
        # Botones de archivos
        file_buttons = ttk.Frame(parent)
        file_buttons.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Button(file_buttons, text="Agregar archivo(s)", command=self.add_files).pack(side=tk.LEFT, padx=2)
        ttk.Button(file_buttons, text="Quitar seleccionado", command=self.remove_file).pack(side=tk.LEFT, padx=2)
        
        # Botón enviar
        ttk.Button(parent, text="Enviar correo", command=self.send_email).grid(row=4, column=1, pady=10)
    
    def create_receive_tab(self, parent):
        """Crea la pestaña de recepción"""
        # Botón refrescar
        refresh_frame = ttk.Frame(parent)
        refresh_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(refresh_frame, text="Actualizar correos", command=self.refresh_emails).pack(side=tk.LEFT)
        
        # Lista de correos
        ttk.Label(parent, text="Correos recibidos:").pack(anchor=tk.W, padx=5, pady=2)
        
        list_frame = ttk.Frame(parent)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.email_listbox = tk.Listbox(list_frame, height=10)
        scrollbar1 = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.email_listbox.yview)
        self.email_listbox.config(yscrollcommand=scrollbar1.set)
        self.email_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar1.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.email_listbox.bind('<Double-Button-1>', self.download_attachments)
        
        # Info de correo seleccionado
        info_frame = ttk.LabelFrame(parent, text="Detalles")
        info_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.email_info = scrolledtext.ScrolledText(info_frame, height=6, wrap=tk.WORD)
        self.email_info.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Botón descargar
        ttk.Button(parent, text="Descargar adjuntos del correo seleccionado", 
                  command=self.download_attachments).pack(pady=5)
        
        self.email_data = []
    
    def load_credentials(self):
        """Carga las credenciales de OAuth2"""
        creds = None
        if os.path.exists(TOKEN_FILE):
            with open(TOKEN_FILE, 'rb') as token:
                creds = pickle.load(token)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(CREDENTIALS_FILE):
                    self.status_var.set("Error: No se encuentra credentials.json. Por favor configura la autenticación.")
                    messagebox.showerror("Error", 
                                       f"No se encuentra {CREDENTIALS_FILE}.\n"
                                       "Por favor descarga las credenciales desde Google Cloud Console.")
                    return
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
                creds = flow.run_local_server(port=0)
            
            with open(TOKEN_FILE, 'wb') as token:
                pickle.dump(creds, token)
        
        try:
            self.service = build('gmail', 'v1', credentials=creds)
            self.status_var.set("Conectado a Gmail")
        except Exception as e:
            self.status_var.set(f"Error de conexión: {str(e)}")
            messagebox.showerror("Error", f"No se pudo conectar a Gmail: {str(e)}")
    
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
    
    def send_email(self):
        """Envía el correo con los archivos adjuntos"""
        if not self.service:
            messagebox.showerror("Error", "No hay conexión con Gmail. Verifica las credenciales.")
            return
        
        if not self.selected_files:
            messagebox.showwarning("Advertencia", "No hay archivos seleccionados.")
            return
        
        to_email = self.to_entry.get().strip()
        subject = self.subject_entry.get().strip()
        
        if not to_email:
            messagebox.showwarning("Advertencia", "El campo 'Para' está vacío.")
            return
        
        def send_thread():
            try:
                self.status_var.set("Enviando correo...")
                message = MIMEMultipart()
                message['To'] = to_email
                message['Subject'] = subject
                message['From'] = DEFAULT_EMAIL
                
                body = "Archivos adjuntos enviados desde App Email Portable"
                message.attach(MIMEText(body, 'plain'))
                
                # Adjuntar archivos
                for file_path in self.selected_files:
                    with open(file_path, 'rb') as f:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(f.read())
                        encoders.encode_base64(part)
                        part.add_header('Content-Disposition', 
                                      f'attachment; filename={os.path.basename(file_path)}')
                        message.attach(part)
                
                raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
                send_message = {'raw': raw_message}
                
                self.service.users().messages().send(userId='me', body=send_message).execute()
                
                self.root.after(0, lambda: self.status_var.set("Correo enviado exitosamente"))
                self.root.after(0, lambda: messagebox.showinfo("Éxito", "Correo enviado exitosamente"))
                
                # Limpiar lista
                self.root.after(0, lambda: self.file_listbox.delete(0, tk.END))
                self.root.after(0, lambda: setattr(self, 'selected_files', []))
                
            except HttpError as error:
                error_msg = f"Error al enviar correo: {error}"
                self.root.after(0, lambda: self.status_var.set(error_msg))
                self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
            except Exception as e:
                error_msg = f"Error inesperado: {str(e)}"
                self.root.after(0, lambda: self.status_var.set(error_msg))
                self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
        
        threading.Thread(target=send_thread, daemon=True).start()
    
    def refresh_emails(self):
        """Actualiza la lista de correos"""
        if not self.service:
            messagebox.showerror("Error", "No hay conexión con Gmail.")
            return
        
        def refresh_thread():
            try:
                self.root.after(0, lambda: self.status_var.set("Obteniendo correos..."))
                
                query = f'to:{DEFAULT_EMAIL} has:attachment'
                results = self.service.users().messages().list(userId='me', q=query, maxResults=20).execute()
                messages = results.get('messages', [])
                
                self.email_data = []
                email_list = []
                
                for msg in messages:
                    message = self.service.users().messages().get(userId='me', id=msg['id']).execute()
                    payload = message['payload']
                    headers = payload.get('headers', [])
                    
                    subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'Sin asunto')
                    sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Desconocido')
                    date = next((h['value'] for h in headers if h['name'] == 'Date'), '')
                    
                    email_list.append(f"{sender[:30]} - {subject[:40]}")
                    self.email_data.append({
                        'id': msg['id'],
                        'subject': subject,
                        'from': sender,
                        'date': date,
                        'payload': payload
                    })
                
                self.root.after(0, lambda: self.update_email_listbox(email_list))
                self.root.after(0, lambda: self.status_var.set(f"Se encontraron {len(messages)} correos con adjuntos"))
                
            except Exception as e:
                error_msg = f"Error al obtener correos: {str(e)}"
                self.root.after(0, lambda: self.status_var.set(error_msg))
                self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
        
        threading.Thread(target=refresh_thread, daemon=True).start()
    
    def update_email_listbox(self, email_list):
        """Actualiza el listbox de correos"""
        self.email_listbox.delete(0, tk.END)
        for email in email_list:
            self.email_listbox.insert(tk.END, email)
    
    def download_attachments(self, event=None):
        """Descarga los adjuntos del correo seleccionado"""
        if not self.service:
            messagebox.showerror("Error", "No hay conexión con Gmail.")
            return
        
        selection = self.email_listbox.curselection()
        if not selection:
            messagebox.showwarning("Advertencia", "Por favor selecciona un correo.")
            return
        
        index = selection[0]
        email = self.email_data[index]
        
        # Actualizar info
        info_text = f"De: {email['from']}\n"
        info_text += f"Asunto: {email['subject']}\n"
        info_text += f"Fecha: {email['date']}\n"
        self.email_info.delete(1.0, tk.END)
        self.email_info.insert(1.0, info_text)
        
        def download_thread():
            try:
                self.root.after(0, lambda: self.status_var.set("Descargando adjuntos..."))
                
                # Obtener el mensaje completo
                message = self.service.users().messages().get(userId='me', id=email['id']).execute()
                payload = message['payload']
                
                # Seleccionar directorio de descarga
                download_dir = filedialog.askdirectory(title="Seleccionar carpeta para descargar")
                if not download_dir:
                    self.root.after(0, lambda: self.status_var.set("Descarga cancelada"))
                    return
                
                # Función recursiva para obtener adjuntos
                def get_attachments(part):
                    attachments = []
                    # Si tiene partes, buscar recursivamente
                    if part.get('parts'):
                        for p in part['parts']:
                            attachments.extend(get_attachments(p))
                    # Si tiene un attachmentId, es un adjunto
                    elif part.get('body') and part['body'].get('attachmentId'):
                        attachments.append(part)
                    return attachments
                
                attachments = get_attachments(payload)
                
                if not attachments:
                    self.root.after(0, lambda: messagebox.showinfo("Info", "Este correo no tiene adjuntos."))
                    self.root.after(0, lambda: self.status_var.set("Sin adjuntos"))
                    return
                
                # Descargar cada adjunto
                downloaded = 0
                for part in attachments:
                    attachment_id = part['body']['attachmentId']
                    filename = part.get('filename', 'adjunto_sin_nombre')
                    
                    attachment = self.service.users().messages().attachments().get(
                        userId='me', messageId=email['id'], id=attachment_id).execute()
                    
                    file_data = base64.urlsafe_b64decode(attachment['data'].encode('UTF-8'))
                    file_path = os.path.join(download_dir, filename)
                    
                    # Evitar sobrescribir
                    counter = 1
                    base_name, ext = os.path.splitext(filename)
                    while os.path.exists(file_path):
                        file_path = os.path.join(download_dir, f"{base_name}_{counter}{ext}")
                        counter += 1
                    
                    with open(file_path, 'wb') as f:
                        f.write(file_data)
                    
                    downloaded += 1
                
                self.root.after(0, lambda: self.status_var.set(f"Descargados {downloaded} archivo(s)"))
                self.root.after(0, lambda: messagebox.showinfo("Éxito", 
                    f"Se descargaron {downloaded} archivo(s) en:\n{download_dir}"))
                
            except Exception as e:
                error_msg = f"Error al descargar: {str(e)}"
                self.root.after(0, lambda: self.status_var.set(error_msg))
                self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
        
        threading.Thread(target=download_thread, daemon=True).start()


def main():
    root = tk.Tk()
    app = EmailApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()

