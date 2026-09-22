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
# Tu banner principal exacto
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
    """Mapeo completo de todos los modelos de iFree con las imágenes exactas de tu GitHub"""
    if not modelo_api:
        return None
        
    m = modelo_api.lower()
    
    # Modelos más nuevos y específicos primero para evitar cruces
    if "17 pro max" in m:
        return GITHUB_BASE_URL + "iphone-17-pro-max.png"
    elif "17 pro" in m:
        return GITHUB_BASE_URL + "iphone-17-pro.png"
    elif "17" in m:
        return GITHUB_BASE_URL + "iphone-17.png"
    elif "16 pro max" in m:
        return GITHUB_BASE_URL + "iphone-16-pro-max.png"
    elif "16 pro" in m:
        return GITHUB_BASE_URL + "iphone-16-pro.png"
    elif "16 plus" in m:
        return GITHUB_BASE_URL + "iphone-16-plus.png"
    elif "16" in m:
        return GITHUB_BASE_URL + "iphone-16.png"
    elif "15 pro max" in m:
        return GITHUB_BASE_URL + "iphone-15-pro-max.png"
    elif "15 pro" in m:
        return GITHUB_BASE_URL + "iphone-15-pro.png"
    elif "15 plus" in m:
        return GITHUB_BASE_URL + "iphone-15-plus.png"
    elif "15" in m:
        return GITHUB_BASE_URL + "iphone-15.png"
    elif "14 pro max" in m:
        return GITHUB_BASE_URL + "iphone-14-pro-max.png"
    elif "14 pro" in m:
        return GITHUB_BASE_URL + "iphone-14-pro.png"
    elif "14 plus" in m:
        return GITHUB_BASE_URL + "iphone-14-plus.png"
    elif "14" in m:
        return GITHUB_BASE_URL + "iphone-14.png"
    elif "13 pro max" in m:
        return GITHUB_BASE_URL + "iphone-13-pro-max.png"
    elif "13 pro" in m:
        return GITHUB_BASE_URL + "iphone-13-pro.png"
    elif "13 mini" in m:
        return GITHUB_BASE_URL + "iphone13-mini.png"
    elif "13" in m:
        return GITHUB_BASE_URL + "iphone13.png"
    elif "12 mini" in m:
        return GITHUB_BASE_URL + "iphone12-mini.png"
    elif "12 pro max" in m:
        return GITHUB_BASE_URL + "iphone12-pro-max.png"
    elif "12 pro" in m:
        return GITHUB_BASE_URL + "iphone12-pro.png"
    elif "12" in m:
        return GITHUB_BASE_URL + "iphone12.png"
    elif "11 pro max" in m:
        return GITHUB_BASE_URL + "iphone-11pro-max.png"
    elif "11 pro" in m:
        return GITHUB_BASE_URL + "iphone-11pro.png"
    elif "11" in m:
        return GITHUB_BASE_URL + "iphone-11.png"
    elif "se (3rd" in m or "se 3" in m:
        return GITHUB_BASE_URL + "iphone-se-3rd-gen.png"
    elif "se (2nd" in m or "se 2" in m:
        return GITHUB_BASE_URL + "iphone-se-2nd-gen.png"
    elif "xs max" in m:
        return GITHUB_BASE_URL + "iphone-xs-max.png"
    elif "xs" in m:
        return GITHUB_BASE_URL + "iphone-xs.png"
    elif "xr" in m:
        return GITHUB_BASE_URL + "iphone-xr.png"
    elif "x" in m:
        return GITHUB_BASE_URL + "iphone-x.png"
    elif "8 plus" in m:
        return GITHUB_BASE_URL + "iphone-8plus.png"
    elif "8" in m:
        return GITHUB_BASE_URL + "iphone-8.png"
    elif "7 plus" in m:
        return GITHUB_BASE_URL + "iphone-7-plus.png"
    elif "7" in m:
        return GITHUB_BASE_URL + "iphone-7.png"
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
            
            # Timeout ampliado a 40 segundos para evitar cortes con consultas pesadas
            response = requests.post(url, data=payload, timeout=40)
            data = response.json()
            
            # Borramos el mensaje de "Consultando..."
            bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id)
            
            if data.get("success") == True:
                result = data.get("object", {})
                modelo = result.get('model', 'N/A')
                marca = result.get('brand', 'Apple')
                fmi = result.get('fmi', result.get('find_my_iphone', 'N/A'))
                
                # 1. ENVIAR TU BANNER PRINCIPAL CON EL TÍTULO EXACTO
                texto_banner = "🌟 **NIRVANA CHECK PREMIUM** 🌟\n*Resultado oficial de tu consulta*"
                bot.send_photo(message.chat.id, BANNER_URL, caption=texto_banner, parse_mode="Markdown")
                
                # Buscamos la foto específica del iPhone correspondiente
                foto_modelo = obtener_url_imagen(modelo)
                
                detalle_respuesta = (
                    f"✅ **Detalles del Dispositivo**\n\n"
                    f"📱 **Modelo:** {modelo}\n"
                    f"🏷️ **Marca:** {marca}\n"
                    f"🔒 **FMI / iCloud:** {fmi}\n"
                    f"📋 **IMEI:** {imei}"
                )
                
                if foto_modelo:
                    # 2. ENVIAR LA FOTO DEL MODELO CON SUS DATOS
                    bot.send_photo(message.chat.id, foto_modelo, caption=detalle_respuesta, parse_mode="Markdown")
                else:
                    bot.send_message(message.chat.id, detalle_respuesta, parse_mode="Markdown")
                
            else:
                error_msg = data.get("error", "Error desconocido en la API")
                bot.send_photo(message.chat.id, BANNER_URL, caption="🌟 **NIRVANA CHECK PREMIUM**", parse_mode="Markdown")
                bot.send_message(message.chat.id, f"❌ Error en la consulta: {error_msg}")
            
        except Exception as e:
            bot.send_message(message.chat.id, "❌ Error de conexión con la API (tiempo de espera agotado).")
    else:
        bot.reply_to(message, "❌ Por favor, envíame un IMEI válido de exactamente 15 dígitos.")

if __name__ == '__main__':
    keep_alive()
    bot.infinity_polling()
