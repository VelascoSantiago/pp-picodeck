import os
import discord
from discord.ext import tasks
import serial
import psutil
from dotenv import load_dotenv

PUERTO_SERIAL = 'COM5' # Confirma que siga siendo tu puerto
BAUD_RATE = 115200

try:
    pico = serial.Serial(PUERTO_SERIAL, BAUD_RATE, timeout=1)
    print(f"[Hardware] Conectado a PicoDeck en {PUERTO_SERIAL}")
except Exception as e:
    print(f"[Error] No se pudo abrir el puerto serial: {e}")
    pico = None

class PicoDeckClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def setup_hook(self):
        # Inicia el bucle secundario para extraer datos del PC
        self.enviar_estadisticas_pc.start()

    async def on_ready(self):
        print(f'[API] Bot {self.user} conectado. Sistema de telemetría iniciado.')

    async def on_message(self, message):
        if message.author == self.user:
            return

        texto_notificacion = ""
        if message.guild is None:
            texto_notificacion = f"DM de {message.author.name[:5]}:\n{message.content}"
        elif message.channel.name in ["general", "alertas"]: 
            texto_notificacion = f"{message.author.name}:\n{message.content}"

        if texto_notificacion and pico and pico.is_open:
            texto_limpio = texto_notificacion.replace('\n', ' ') 
            # Inyectamos el prefijo D| para enrutar a Discord
            pico.write((f"D|{texto_limpio}\r\n").encode('utf-8'))
            print(f"[Discord] -> {texto_limpio}")

    # Este bloque extrae métricas de CPU/RAM cada 2 segundos en segundo plano
    @tasks.loop(seconds=2)
    async def enviar_estadisticas_pc(self):
        if pico and pico.is_open:
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory().percent
            
            # Inyectamos el prefijo O| y separamos renglones con |
            pico.write((f"O|CPU: {cpu}%|RAM: {ram}%\r\n").encode('utf-8'))

# --- INICIALIZACIÓN ---
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

cliente = PicoDeckClient(intents=intents)

if __name__ == '__main__':
    if TOKEN is None:
        print("[Error] Falla al cargar el Token.")
    else:
        cliente.run(TOKEN)