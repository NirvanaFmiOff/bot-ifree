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
            url = "https://ifreeicloud.co.uk/api"
            params = {"key": IFREE_API_KEY, "imei": imei}
            response = requests.get(url, params=params, timeout=20)
            data = response.json()
            
            if data.get("status") == 250 or data.get("success") == True:
                result = data.get("object", data)
                respuesta = (
                    f"✅ **Resultado de la consulta**\n\n"
                    f"📱 **Modelo:** {result.get('model', 'N/A')}\n"
                    f"🏷️ **Marca:** {result.get('brand', 'Apple')}\n"
                    f"🔒 **FMI / iCloud:** {result.get('fmi', result.get('find_my_iphone', 'N/A'))}\n"
                    f"📋 **IMEI:** {imei}"
                )
            else:
                respuesta = f"❌ Error: {data.get('error', 'Respuesta no válida')}"
            
            bot.edit_message_text(respuesta, chat_id=message.chat.id, message_id=msg.message_id, parse_mode="Markdown")
            
        except Exception as e:
            bot.edit_message_text(f"❌ Error de conexión con la API.", chat_id=message.chat.id, message_id=msg.message_id)
    else:
        bot.reply_to(message, "❌ Envía un IMEI válido de 15 dígitos.")

if __name__ == '__main__':
    keep_alive()
    bot.infinity_polling()
