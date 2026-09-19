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
    bot.reply_to(message, "¡Hola! Envíame tu código IMEI de 15 dígitos para consultarlo en iFree.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    imei = message.text.strip()
    
    if imei.isdigit() and len(imei) == 15:
        msg = bot.reply_to(message, f"🔍 Consultando el IMEI: {imei}...")
        
        try:
            # Endpoint y parámetros exactos basados en la documentación oficial de iFree
            url = "https://api.ifreeicloud.co.uk/"
            payload = {
                "service": 0,
                "imei": imei,
                "key": IFREE_API_KEY
            }
            
            response = requests.post(url, data=payload, timeout=20)
            data = response.json()
            
            # Validamos según la estructura oficial (success == true)
            if data.get("success") == True:
                result = data.get("object", {})
                modelo = result.get('model', 'N/A')
                marca = result.get('brand', 'Apple')
                fmi = result.get('fmi', result.get('find_my_iphone', 'N/A'))
                
                respuesta = (
                    f"✅ **Resultado de la consulta**\n\n"
                    f"📱 **Modelo:** {modelo}\n"
                    f"🏷️ **Marca:** {marca}\n"
                    f"🔒 **FMI / iCloud:** {fmi}\n"
                    f"📋 **IMEI:** {imei}"
                )
            else:
                error_msg = data.get("error", "Error desconocido en la API")
                respuesta = f"❌ Error en la consulta: {error_msg}"
            
            bot.edit_message_text(respuesta, chat_id=message.chat.id, message_id=msg.message_id, parse_mode="Markdown")
            
        except Exception as e:
            bot.edit_message_text(f"❌ Error de conexión con la API.", chat_id=message.chat.id, message_id=msg.message_id)
    else:
        bot.reply_to(message, "❌ Por favor, envíame un IMEI válido de exactamente 15 dígitos.")

if __name__ == '__main__':
    keep_alive()
    bot.infinity_polling()
