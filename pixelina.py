import os
import random
import telebot
from flask import Flask, request

TOKEN = os.environ.get("PIXELINA_TOKEN")
if not TOKEN:
    raise ValueError("PIXELINA_TOKEN no definido en variables de entorno")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# -------------------------------
# MENÚ
def main_menu():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("📶 WiFi Escolar", "📚 Tareas")
    markup.row("👨‍🏫 ¿Dónde está el profe?", "🔮 Oráculo Tecno")
    markup.row("💡 Sugerencias", "🆘 Ayuda")
    markup.row("🗓 Calendario", "📣 Novedades", "💻 Proyectos")
    return markup

# -------------------------------
# RESPUESTAS
wifi_msgs = ["¡No es tu compu! El WiFi del cole está tomando mate ☕",
             "Red inestable… alguien desconectó los cables para jugar a la escondida 🕵️‍♂️",
             "¡Ups! El WiFi se fue de recreo 🏃💨"]

tareas_msgs = ["¿Tenés tareas pendientes? ¡A por ellas! 📘💪",
               "Recordá anotar las tareas en la libreta digital 📓✨"]

profe_msgs = ["Está en la sala de profesores 📋, con cara de misterio 🤨",
              "¡Fue al kiosco! 😄 Probá ir con monedas 🪙"]

oraculo_msgs = ["Hoy aprenderás algo nuevo sobre IA 🤖",
                "¡Tu código va a compilar sin errores! 💻",
                "Un bug oculto aparecerá en tu proyecto 👻",
                "Recibirás una gran idea para tu maqueta escolar 🧠",
                "Alguien intentará hackear tu proyecto… ¡con amor! ❤️💾"]

# -------------------------------
# SALUDOS
greetings = ["hola", "buen día", "buenos días", "buenas", "hey", "hi", "hello"]

# -------------------------------
# HANDLERS
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     "👋 ¡Hola! Soy *PixelinaBot*, tu asistente escolar 🤖.\n"
                     "Elegí una opción del menú 👇",
                     parse_mode="Markdown",
                     reply_markup=main_menu())

@bot.message_handler(func=lambda m: any(greet in m.text.lower() for greet in greetings))
def saludo(message):
    bot.send_message(message.chat.id, "¡Hola! 👋 PixelinaBot está lista para ayudarte 😎", reply_markup=main_menu())

@bot.message_handler(func=lambda m: True)
def responder_mensajes(message):
    txt = message.text.lower()

    if "wifi" in txt:
        bot.send_message(message.chat.id, random.choice(wifi_msgs))
    elif "tareas" in txt:
        bot.send_message(message.chat.id, random.choice(tareas_msgs))
    elif "profe" in txt:
        bot.send_message(message.chat.id, random.choice(profe_msgs))
    elif "oráculo" in txt or "oraculo" in txt:
        bot.send_message(message.chat.id, random.choice(oraculo_msgs))
    elif "sugerencia" in txt or "💡" in txt:
        bot.send_message(message.chat.id, "✍️ Guardaré tu sugerencia (simulación).")
    elif "ayuda" in txt or "🆘" in txt:
        bot.send_message(message.chat.id, "📨 Escribí tu consulta y alguien del equipo la verá.")
    elif "calendario" in txt or "🗓" in txt:
        bot.send_message(message.chat.id, "📅 Próxima entrega: viernes 19/07")
    elif "novedades" in txt or "📣" in txt:
        bot.send_message(message.chat.id, "🆕 ¡Se viene un torneo de robótica! 🤖")
    elif "proyectos" in txt or "💻" in txt:
        bot.send_message(message.chat.id, "🚀 PixelinaBot: maquetas automatizadas, apps y más. ¡Sumate! 🤩")
    elif any(x in txt for x in ["chau","adios","me voy","chao"]):
        bot.send_message(message.chat.id, "👋 ¡Hasta pronto! PixelinaBot estará por acá cuando me necesites.")
    else:
        bot.send_message(message.chat.id, "No entendí eso 🤖. Probá con el menú 👇", reply_markup=main_menu())

# -------------------------------
# FLASK WEBHOOK
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = telebot.types.Update.de_json(request.get_data().decode("utf-8"))
    bot.process_new_updates([update])
    return "OK", 200

@app.route("/")
def home():
    return "PixelinaBot está activo en Render 🚀"

# -------------------------------
# SETEAR WEBHOOK AUTOMÁTICAMENTE
render_url = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if render_url:
    bot.remove_webhook()
    bot.set_webhook(url=f"https://{render_url}/{TOKEN}")
    print("✅ Webhook seteado en:", f"https://{render_url}/{TOKEN}")
else:
    print("❌ No se encontró RENDER_EXTERNAL_HOSTNAME. Revisá variables de entorno.")

# -------------------------------
# CORRER FLASK
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
