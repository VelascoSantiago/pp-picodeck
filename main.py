from machine import Pin, I2C
import time
from machine_i2c_lcd import I2cLcd

# --- 1. CONFIGURACIÓN DE HARDWARE ---
led_verde = Pin(16, Pin.OUT)
led_amarillo = Pin(17, Pin.OUT)
led_rojo = Pin(18, Pin.OUT)

buzzer = Pin(19, Pin.OUT)
boton = Pin(15, Pin.IN, Pin.PULL_UP)

# --- 2. CONFIGURACIÓN DE LA PANTALLA LCD ---
# Usamos GP0 (SDA) y GP1 (SCL)
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)

# Buscamos la dirección I2C automáticamente y configuramos la pantalla (16 columnas, 2 filas)
direccion_i2c = i2c.scan()[0]
lcd = I2cLcd(i2c, direccion_i2c, 2, 16)

# --- 3. DEFINICIÓN DE ESTADOS ---
MODO_DISCORD = 0
MODO_OVERLAY = 1
MODO_OFFLINE = 2

estado_actual = MODO_DISCORD

# --- 4. FUNCIONES DE LÓGICA ---
def cambiar_estado():
    global estado_actual
    estado_actual += 1
    
    if estado_actual > MODO_OFFLINE:
        estado_actual = MODO_DISCORD
        
    if estado_actual != MODO_OFFLINE:
        buzzer.value(1)
        time.sleep(0.01) # Clic háptico corto
        buzzer.value(0)

def actualizar_hardware():
    led_verde.value(0)
    led_amarillo.value(0)
    led_rojo.value(0)
    lcd.clear() # Limpiamos la pantalla antes de escribir lo nuevo
    
    if estado_actual == MODO_DISCORD:
        led_verde.value(1)
        lcd.move_to(0, 0) # Columna 0, Fila 0 (Arriba)
        lcd.putstr("Modo Discord")
        lcd.move_to(0, 1) # Columna 0, Fila 1 (Abajo)
        lcd.putstr("Escuchando...")
        
    elif estado_actual == MODO_OVERLAY:
        led_amarillo.value(1)
        lcd.move_to(0, 0)
        lcd.putstr("Modo Overlay")
        lcd.move_to(0, 1)
        lcd.putstr("Esperando PC...")
        
    elif estado_actual == MODO_OFFLINE:
        led_rojo.value(1)
        lcd.move_to(0, 0)
        lcd.putstr("[ Sistema ]")
        lcd.move_to(0, 1)
        lcd.putstr("[ Inactivo ]")

# --- 5. INICIALIZACIÓN Y BUCLE PRINCIPAL ---
lcd.putstr("Iniciando Hub...")
time.sleep(1)
actualizar_hardware()

while True:
    if boton.value() == 0:
        cambiar_estado()
        actualizar_hardware()
        time.sleep(0.3) 
        
    time.sleep(0.05)