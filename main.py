from machine import Pin, I2C
import time
import sys
import select
from machine_i2c_lcd import I2cLcd

# --- 1. CONFIGURACIÓN DE HARDWARE ---
led_verde = Pin(16, Pin.OUT)
led_amarillo = Pin(17, Pin.OUT)
led_rojo = Pin(18, Pin.OUT)
buzzer = Pin(20, Pin.OUT) # Pin 20 según tu diagrama
boton = Pin(15, Pin.IN, Pin.PULL_UP)

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
direccion_i2c = i2c.scan()[0]
lcd = I2cLcd(i2c, direccion_i2c, 2, 16)

# --- 2. CONFIGURACIÓN SERIAL (USB) ---
usb_serial = select.poll()
usb_serial.register(sys.stdin, select.POLLIN)

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
        
    # El clic háptico suena en TODOS los cambios de estado
    buzzer.value(1)
    time.sleep(0.01) 
    buzzer.value(0)

def actualizar_interfaz():
    led_verde.value(0)
    led_amarillo.value(0)
    led_rojo.value(0)
    lcd.clear()
    
    if estado_actual == MODO_DISCORD:
        led_verde.value(1)
        lcd.move_to(0,0)
        lcd.putstr("Modo Discord")
        lcd.move_to(0,1)
        lcd.putstr("Esperando msj...")
        
    elif estado_actual == MODO_OVERLAY:
        led_amarillo.value(1)
        lcd.move_to(0,0)
        lcd.putstr("Modo Overlay")
        lcd.move_to(0,1)
        lcd.putstr("Esperando PC...")
        
    elif estado_actual == MODO_OFFLINE:
        led_rojo.value(1)
        lcd.move_to(0,0)
        lcd.putstr("[ Sistema ]")
        lcd.move_to(0,1)
        lcd.putstr("[ Inactivo ]")

def procesar_datos_pc():
    if usb_serial.poll(0): 
        mensaje = sys.stdin.readline().strip() 
        
        if estado_actual != MODO_OFFLINE and mensaje:
            lcd.clear()
            lcd.move_to(0,0)
            lcd.putstr(mensaje[:16]) 
            
            buzzer.value(1)
            time.sleep(0.05)
            buzzer.value(0)

# --- 5. INICIALIZACIÓN ---
lcd.clear()
lcd.move_to(0,0)
lcd.putstr("Conectando USB..")
time.sleep(1)
actualizar_interfaz()

# --- 6. BUCLE PRINCIPAL ---
while True:
    if boton.value() == 0:
        cambiar_estado()
        actualizar_interfaz()
        time.sleep(0.3)
        
    procesar_datos_pc()
        
    time.sleep(0.05)