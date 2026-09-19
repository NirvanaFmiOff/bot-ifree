import os
import telebot
from flask import Flask
from threading import Thread

# Cargamos el token del bot de forma segura desde las variables de entorno
TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# Servidor Flask básico para mantener el servicio activo en Render (evita que se duerma)
app = Flask('')

@app.route('/')
def home():
    return "¡El bot de iFree IMEI está activo y funcionando 24/7!"

def run():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()

# Comando de bienvenida
@bot.message_handler(commands=['start', 'help'])
def send_welcome(bot_message):
    bot.reply_to(bot_message, "¡Hola! Envíame tu código IMEI para procesarlo a través de la API de iFree.")

# Manejador básico de mensajes (aquí conectaremos la API de iFree)
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    imei = message.text.strip()
    
    # Verificamos si parece un IMEI válido (15 dígitos)
    if imei.isdigit() and len(imei) == 15:
        bot.reply_to(message, f"🔍 Procesando IMEI: `{imei}`...\nPor favor espera un momento.", parse_mode="Markdown")
        # Aquí agregaremos la consulta a la API de iFree con tu llave: SYE-VKS-E4U-9CR-TZB-X68-7YH-ID4
    else:
        bot.reply_to(message, "❌ Por favor, envía un número de IMEI válido de 15 dígitos.")

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
