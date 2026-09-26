import os
import telebot
import requests
from flask import Flask
from threading import Thread

TOKEN = os.getenv('BOT_TOKEN')
IFREE_API_KEY = "SYE-VKS-E4U-9CR-TZB-X68-7YH-ID4"
bot = telebot.TeleBot(TOKEN)

# ⚠️ TU CANAL OFICIAL CONFIGURADO
CANAL_ID = "@NirvanaInfinitoOficial" 

app = Flask('')

# Tu URL base de GitHub Pages
GITHUB_BASE_URL = "https://nirvanafmioff.github.io/Catalogonirvana/"
BANNER_URL = GITHUB_BASE_URL + "tu-banner.jpg"

@app.route('/')
def home():
    return "Bot activo"

def run():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()

def verificar_membresia(user_id):
    """Verifica si el usuario forma parte del canal oficial"""
    try:
        chat_member = bot.get_chat_member(CANAL_ID, user_id)
        estados_validos = ['creator', 'administrator', 'member']
        return chat_member.status in estados_validos
    except Exception as e:
        print(f"Error al verificar membresía: {e}")
        return False

def obtener_url_imagen(modelo_api):
    """Mapeo sincronizado exactamente con los nombres del HTML de GitHub"""
    if not modelo_api:
        return None
        
    m = modelo_api.lower()
    
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
        return GITHUB_BASE_URL + "iphone-13-mini.png"
    elif "13" in m:
        return GITHUB_BASE_URL + "iphone-13.png"
    elif "12 mini" in m:
        return GITHUB_BASE_URL + "iphone-12-mini.png"
    elif "12 pro max" in m:
        return GITHUB_BASE_URL + "iphone-12-pro-max.png"
    elif "12 pro" in m:
        return GITHUB_BASE_URL + "iphone-12-pro.png"
    elif "12" in m:
        return GITHUB_BASE_URL + "iphone-12.png"
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
    user_id = message.from_user.id
    
    if not verificar_membresia(user_id):
        bot.reply_to(
            message, 
            "🛡️ **SISTEMA PROTEGIDO — NIRVANA INFINITO** ♾️\n\n"
            "_Acceso denegado._ Propiedad exclusiva de Nirvana Infinito. No tienes acceso.\n\n"
            "Únete al canal oficial y da un like para poder usar el bot.",
            parse_mode="Markdown"
        )
        return

    bot.reply_to(message, "♾️ **NIRVANA CHECK SYSTEM** ♾️\n\nEnvíame el código IMEI de 15 dígitos del dispositivo para procesar la verificación oficial.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    
    if not verificar_membresia(user_id):
        bot.reply_to(
            message, 
            "🛡️ **SISTEMA PROTEGIDO — NIRVANA INFINITO** ♾️\n\n"
            "_Acceso restringido._ No posees autorización para operar este sistema.\n\n"
            "Únete al canal oficial y da un like para poder usar el bot.",
            parse_mode="Markdown"
        )
        return

    imei = message.text.strip()
    
    if imei.isdigit() and len(imei) == 15:
        msg = bot.reply_to(message, f"🔍 Procesando verificación del dispositivo: {imei}...")
        
        try:
            url = "https://api.ifreeicloud.co.uk/"
            payload = {
                "service": 0,
                "imei": imei,
                "key": IFREE_API_KEY
            }
            
            response = requests.post(url, data=payload, timeout=40)
            bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id)
            
            try:
                data = response.json()
            except Exception as json_err:
                print(f"Error al parsear JSON: {json_err} - Respuesta cruda: {response.text}")
                bot.send_message(message.chat.id, "❌ Error: El servidor devolvió una respuesta con formato inválido.")
                return

            print(f"Respuesta de API para IMEI {imei}: {data}")

            success_val = data.get("success")
            is_success = success_val is True or str(success_val).lower() == "true"

            if is_success:
                result = data.get("object", {})
                
                # Extracción segura adaptada para la familia 13 y otros modelos
                modelo = result.get('model') or result.get('modelName') or 'Apple iPhone'
                marca = result.get('brand', 'Apple')
                fmi = result.get('fmi') or result.get('find_my_iphone') or 'N/A'
                
                texto_banner = "🌟 **NIRVANA CHECK PREMIUM** 🌟\n*Resultado oficial de tu consulta*"
                bot.send_photo(message.chat.id, BANNER_URL, caption=texto_banner, parse_mode="Markdown")
                
                foto_modelo = obtener_url_imagen(modelo)
                
                detalle_respuesta = (
                    f"✅ **Detalles del Dispositivo**\n\n"
                    f"📱 **Modelo:** {modelo}\n"
                    f"🏷️ **Marca:** {marca}\n"
                    f"🔒 **FMI / iCloud:** {fmi}\n"
                    f"📋 **IMEI:** {imei}"
                )
                
                if foto_modelo:
                    bot.send_photo(message.chat.id, foto_modelo, caption=detalle_respuesta, parse_mode="Markdown")
                else:
                    bot.send_message(message.chat.id, detalle_respuesta, parse_mode="Markdown")
                
            else:
                error_msg = data.get("error", data.get("message", "Error en el sistema"))
                bot.send_photo(message.chat.id, BANNER_URL, caption="🌟 **NIRVANA CHECK PREMIUM**", parse_mode="Markdown")
                bot.send_message(message.chat.id, f"❌ Aviso del sistema: {error_msg}")
        
        except requests.exceptions.Timeout:
            bot.send_message(message.chat.id, "❌ Error de conexión: El servidor tardó demasiado en responder.")
        except Exception as e:
            print(f"Excepción general: {e}")
            bot.send_message(message.chat.id, f"❌ Ocurrió un error inesperado al procesar la solicitud.")
    else:
        bot.reply_to(message, "❌ Por favor, envíame un IMEI válido de exactamente 15 dígitos.")

if __name__ == '__main__':
    keep_alive()
    bot.infinity_polling()
