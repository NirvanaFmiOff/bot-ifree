import os
import telebot
import requests
from flask import Flask
from threading import Thread

TOKEN = os.getenv('BOT_TOKEN')
IFREE_API_KEY = "SYE-VKS-E4U-9CR-TZB-X68-7YH-ID4"
bot = telebot.TeleBot(TOKEN)

app = Flask('')

@app.route('/')
def home():
    return "Bot activo"

def run():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "¡Hola! Envíame tu código IMEI de 15 dígitos.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    imei = message.text.strip()
    
    if imei.isdigit() and len(imei) == 15:
        msg = bot.reply_to(message, f"🔍 Consultando el IMEI: {imei}...")
        
        try:
            url = f"https://ifreeicloud.co.uk/api?key={IFREE_API_KEY}&imei={imei}"
            response = requests.get(url, timeout=20)
            
            # Intentamos convertir la respuesta directamente a JSON
            data = response.json()
            
            # Verificamos si el JSON contiene los datos del equipo
            if data and isinstance(data, dict):
                # Extraemos los campos adaptados al formato JSON de la API
                modelo = data.get('model', data.get('imei_model', 'N/A'))
                marca = data.get('brand', 'Apple')
                fmi = data.get('fmi', data.get('find_my_iphone', data.get('icloud', 'N/A')))
                
                respuesta = (
                    f"✅ **Resultado de la consulta**\n\n"
                    f"📱 **Modelo:** {modelo}\n"
                    f"🏷️ **Marca:** {marca}\n"
                    f"🔒 **FMI / iCloud:** {fmi}\n"
                    f"📋 **IMEI:** {imei}"
                )
            else:
                respuesta = "❌ La API respondió pero el formato JSON no es válido."
            
            bot.edit_message_text(respuesta, chat_id=message.chat.id, message_id=msg.message_id, parse_mode="Markdown")
            
        except Exception as e:
            bot.edit_message_text(f"❌ Error al procesar el JSON de la API: {str(e)}", chat_id=message.chat.id, message_id=msg.message_id)
    else:
        bot.reply_to(message, "❌ Envía un IMEI válido de 15 dígitos.")

if __name__ == '__main__':
    keep_alive()
    bot.infinity_polling()
