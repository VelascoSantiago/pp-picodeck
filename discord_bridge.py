import discord
import serial
import time
import os
from dotenv import load_dotenv

# --- 1. CONFIGURACIÓN DEL PUERTO SERIAL ---
# IMPORTANTE: Revisa en Thonny o en el Administrador de Dispositivos qué puerto COM usa tu Pico
PUERTO_SERIAL = 'COM5' # Cambia esto por tu puerto real (ej. COM4, COM5)
BAUD_RATE = 115200

try:
    # Conectamos con el hardware
    pico = serial.Serial(PUERTO_SERIAL, BAUD_RATE, timeout=1)
    print(f"[Hardware] Conectado a PicoDeck en {PUERTO_SERIAL}")
except Exception as e:
    print(f"[Error] No se pudo abrir el puerto serial: {e}")
    pico = None

# --- 2. CONFIGURACIÓN DEL CLIENTE DE DISCORD ---
class PicoDeckClient(discord.Client):
    async def on_ready(self):
        print(f'[API] Bot {self.user} conectado a Discord y escuchando.')

    async def on_message(self, message):
        # Ignorar los mensajes que envía el propio bot para evitar bucles infinitos
        if message.author == self.user:
            return

        # Limpiamos el texto y lo preparamos
        texto_notificacion = f"{message.author.name}: {message.content}"
        print(f"[Nuevo Mensaje] -> {texto_notificacion}")
        
        # Enviar al hardware
        if pico and pico.is_open:
            # Enviamos el texto codificado en bytes y agregamos un salto de línea (\n)
            # El \n es crucial para que la función readline() de la Pico sepa que el texto terminó
            pico.write((texto_notificacion + '\n').encode('utf-8'))

# --- 3. INICIALIZACIÓN ---
intents = discord.Intents.default()
intents.message_content = True

cliente = PicoDeckClient(intents=intents)

# Cargamos el archivo .env oculto
load_dotenv()

# Sacamos el token de forma segura
TOKEN = os.getenv('DISCORD_TOKEN')

if __name__ == '__main__':
    if TOKEN is None:
        print("[Error] No se encontró el DISCORD_TOKEN en el archivo .env")
    else:
        cliente.run(TOKEN)