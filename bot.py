import os
import telebot
import requests
from flask import Flask
from threading import Thread

TOKEN = os.getenv('BOT_TOKEN')
IFREE_API_KEY = "SYE-VKS-E4U-9CR-TZB-X68-7YH-ID4"
bot = telebot.TeleBot(TOKEN)

app = Flask('')

# Tu URL base de GitHub Pages
GITHUB_BASE_URL = "https://nirvanafmioff.github.io/Catalogonirvana/"
# Tu banner principal nombrado tal cual me dijiste
BANNER_URL = GITHUB_BASE_URL + "tu-banner.jpg"

@app.route('/')
def home():
    return "Bot activo"

def run():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()

def obtener_url_imagen(modelo_api):
    """Mapea el modelo que devuelve iFree con el nombre exacto de la imagen en tu GitHub"""
    if not modelo_api:
        return None
        
    m = modelo_api.lower()
    
    if "11 pro max" in m:
        return GITHUB_BASE_URL + "iphone-11pro-max.png"
    elif "11 pro" in m:
        return GITHUB_BASE_URL + "iphone-11pro.png"
    elif "11" in m:
        return GITHUB_BASE_URL + "iphone-11.png"
    elif "14 plus" in m:
        return GITHUB_BASE_URL + "iphone-14-plus.png"
    elif "14 pro max" in m:
        return GITHUB_BASE_URL + "iphone-14-pro-max.png"
    elif "14 pro" in m:
        return GITHUB_BASE_URL + "iphone-14-pro.png"
    elif "14" in m:
        return GITHUB_BASE_URL + "iphone-14.png"
    elif "15 plus" in m:
        return GITHUB_BASE_URL + "iphone-15-plus.png"
    elif "15 pro max" in m:
        return GITHUB_BASE_URL + "iphone-15-pro-max.png"
    else:
        return None

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "¡Hola! Envíame tu código IMEI de 15 dígitos para consultarlo en iFree.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    imei = message.text.strip()
    
    if imei.isdigit() and len(imei) == 15:
        msg = bot.reply_to(message, f"🔍 Consultando el IMEI: {imei}...")
        
        try:
            url = "https://api.ifreeicloud.co.uk/"
            payload = {
                "service": 0,
                "imei": imei,
                "key": IFREE_API_KEY
            }
            
            response = requests.post(url, data=payload, timeout=20)
            data = response.json()
            
            # Borramos el mensaje de "Consultando..."
            bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id)
            
            if data.get("success") == True:
                result = data.get("object", {})
                modelo = result.get('model', 'N/A')
                marca = result.get('brand', 'Apple')
                fmi = result.get('fmi', result.get('find_my_iphone', 'N/A'))
                
                # 1. ENVIAR PRIMERO EL BANNER PRINCIPAL
                texto_banner = "🌟 **NIRVANA FMI PREMIUM** 🌟\n*Resultado oficial de tu consulta*"
                bot.send_photo(message.chat.id, BANNER_URL, caption=texto_banner, parse_mode="Markdown")
                
                # Buscamos la foto específica del iPhone
                foto_modelo = obtener_url_imagen(modelo)
                
                detalle_respuesta = (
                    f"✅ **Detalles del Dispositivo**\n\n"
                    f"📱 **Modelo:** {modelo}\n"
                    f"🏷️ **Marca:** {marca}\n"
                    f"🔒 **FMI / iCloud:** {fmi}\n"
                    f"📋 **IMEI:** {imei}"
                )
                
                if foto_modelo:
                    # 2. ENVIAR LA FOTO DEL IPHONE (más chica/específica) con sus datos
                    bot.send_photo(message.chat.id, foto_modelo, caption=detalle_respuesta, parse_mode="Markdown")
                else:
                    # Si la API devolvió un modelo que no está en la lista, mandamos solo el texto con los datos
                    bot.send_message(message.chat.id, detalle_respuesta, parse_mode="Markdown")
                
            else:
                error_msg = data.get("error", "Error desconocido en la API")
                # Si hay error, mandamos el banner y el aviso del error
                bot.send_photo(message.chat.id, BANNER_URL, caption="🌟 **NIRVANA FMI PREMIUM**", parse_mode="Markdown")
                bot.send_message(message.chat.id, f"❌ Error en la consulta: {error_msg}")
            
        except Exception as e:
            bot.send_message(message.chat.id, "❌ Error de conexión con la API.")
    else:
        bot.reply_to(message, "❌ Por favor, envíame un IMEI válido de exactamente 15 dígitos.")

if __name__ == '__main__':
    keep_alive()
    bot.infinity_polling()
