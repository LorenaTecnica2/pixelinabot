import os
import json
import telebot
import gspread
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials
from flask import Flask, request

# --- TOKEN del bot de Telegram ---
TOKEN = os.environ.get("TELEGRAM_TOKEN")  # cargado desde Render
bot = telebot.TeleBot(TOKEN)

# --- Configurar Google Sheets ---
def conectar_sheets():
    json_cred = os.environ.get("GOOGLE_CREDENTIALS_JSON")
    creds_dict = json.loads(json_cred)

    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    sheet = client.open("pixelinacomentarios").sheet1  # nombre exacto de tu hoja
    return sheet

# --- Guardar sugerencia ---
def guardar_sugerencia(message):
    try:
        sheet = conectar_sheets()
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        usuario = f"@{message.from_user.username}" if message.from_user.username else f"{message.from_user.first_name}"
        texto = message.text
        sheet.append_row([fecha, usuario, texto, "Sugerencia"])
        bot.send_message(message.chat.id, "✅ ¡Gracias! Tu sugerencia fue guardada.")
    except Exception as e:
        bot.send_message(message.chat.id, f"⚠️ Error al guardar la sugerencia: {e}")

# --- Mensaje de bienvenida ---

# --- MENSAJE INICIAL ---
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "👋 ¡Hola! Soy *PixelinaBot*, tu asistente escolar 🤖.\nEstoy lista para ayudarte con tareas, proyectos y dudas. Elegí una opción del menú 👇",
        parse_mode="Markdown",
        reply_markup=main_menu()
    )

# --- MENÚ PRINCIPAL ---
def main_menu():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("📶 WiFi Escolar", "📚 Tareas")
    markup.row("👨‍🏫 ¿Dónde está el profe?", "🔮 Oráculo Tecno")
    markup.row("💡 Sugerencias", "🆘 Ayuda")
    markup.row("🗓 Calendario", "📣 Novedades", "💻 Proyectos")
    return markup

# --- RESPUESTAS ALEATORIAS ---
wifi_msgs = ["¡No es tu compu! El WiFi del cole está tomando mate ☕", "Red inestable. Probá moverte."]
tareas_msgs = ["¿Tenés tareas pendientes? ¡Hacelas!", "Acordate de hacerlas 📘"]
profe_msgs = ["Está en preceptoría 📋", "¡Fue al kiosco! 😄", "Lo vi en la esquina 👨‍🔬"]

# --- RESPUESTAS A MENSAJES ---
@bot.message_handler(func=lambda m: True)
def responder_mensajes(message):
    txt = message.text.lower()

    if txt in ["📶 wifi escolar", "wifi"]:
        bot.send_message(message.chat.id, random.choice(wifi_msgs))
    elif txt in ["📚 tareas", "tareas"]:
        bot.send_message(message.chat.id, random.choice(tareas_msgs))
    elif txt in ["👨‍🏫 ¿dónde está el profe?", "donde esta el profe"]:
        bot.send_message(message.chat.id, random.choice(profe_msgs))
    elif txt in ["🔮 oráculo tecno", "oraculo"]:
        predicciones = [
            "Hoy aprenderás algo nuevo sobre IA 🤖",
            "¡Tu código va a compilar sin errores! 💻",
            "Un bug oculto aparecerá en tu proyecto 👻",
            "Recibirás una gran idea para tu maqueta escolar 🧠"
        ]
# --- RESPUESTAS A MENSAJES ---
@bot.message_handler(func=lambda m: True)
def manejar_mensajes(message):
    texto=message.text.lower().strip()

    #---saludos comunes ---#
    saludos=["hola"," buenas", "holi", "hello"]
    despedidas=["chau", "adios", "adiós", " me voy", "nos vemos", "hasta luego"]
    if any(palabra in texto for palabra in saludos):
        bot.send_message(message.chat.id, "🙋‍♀️ ¡Hola! Que alegría verte por acá. ¿Querés dejar una sugerencia, hacer una consult o simplemente saludar")
        return
    elif  any(palabra in texto for palabra in despedidas):
        bot.send_message(message.chat.id, "👋 ¡Hasta pronto! Cuidate mucho y volvé cuando quieras 🌟")
        return
    bot.send.message(message.chat.id,"No te entiendo, seleccioná una opción del menú")


# --- Manejar sugerencias (todo mensaje común) ---


# --- Flask para mantener activo en Render ---
app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "PixelinaBot activo en Render"

@app.route(f"/{TOKEN}", methods=['POST'])
def webhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

# --- Activar webhook (solo la primera vez, o si reiniciás el servidor) ---
bot.remove_webhook()
bot.set_webhook(url=f"https://pixelinabot.onrender.com{TOKEN}")

# --- Iniciar Flask ---
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
