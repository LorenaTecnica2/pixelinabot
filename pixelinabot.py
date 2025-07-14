import os
import random
import telebot
from flask import Flask, request

TOKEN = os.environ.get("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

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
wifi_msgs = ["¡No es tu compu! El WiFi del cole está tomando mate ☕", "Red inestable. Probá moverte de aula."]
tareas_msgs = ["¿Tenés tareas pendientes? ¡A por ellas!", "Recordá anotar las tareas en la libreta digital 📘"]
profe_msgs = ["Está en la sala de profesores 📋", "¡Fue al kiosco! 😄", "Lo vi en el laboratorio 👨‍🔬"]

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
        bot.send_message(message.chat.id, random.choice(predicciones))
    elif txt in ["💡 sugerencias", "sugerencia"]:
        msg = bot.send_message(message.chat.id, "✍️ Escribí tu sugerencia, ¡yo la guardo!")
        bot.register_next_step_handler(msg, guardar_sugerencia)
    elif txt in ["🆘 ayuda", "ayuda"]:
        msg = bot.send_message(message.chat.id, "📨 Escribí tu consulta y alguien del equipo la verá.")
        bot.register_next_step_handler(msg, guardar_consulta)
    elif txt in ["🗓 calendario", "calendario"]:
        bot.send_message(message.chat.id, "📅 Próxima entrega: viernes 19/07.\n⚙️ Reunión de proyecto: lunes 22.")
    elif txt in ["📣 novedades", "novedades"]:
        bot.send_message(message.chat.id, "🆕 ¡Se viene un torneo de robótica! Pronto más info.")
    elif txt in ["💻 proyectos", "proyectos"]:
        bot.send_message(message.chat.id, "🚀 PixelinaBot, maquetas automatizadas y más. ¡Sumate!")
    elif txt in ["chau", "chao", "adios", "me voy"]:
        bot.send_message(message.chat.id, "👋 ¡Hasta pronto! PixelinaBot estará por acá cuando me necesites.")
    else:
        bot.send_message(message.chat.id, "No entendí eso 🤖. Probá con el menú 👇", reply_markup=main_menu())

# --- GUARDAR SUGERENCIAS Y CONSULTAS ---
def guardar_sugerencia(message):
    with open("sugerencias.txt", "a", encoding="utf-8") as f:
        f.write(f"{message.chat.id}: {message.text}\n")
    bot.send_message(message.chat.id, "¡Gracias! Tu sugerencia fue registrada.")

def guardar_consulta(message):
    with open("consultas.txt", "a", encoding="utf-8") as f:
        f.write(f"{message.chat.id}: {message.text}\n")
    bot.send_message(message.chat.id, "Tu mensaje fue enviado. ¡Gracias!")

# --- FLASK PARA WEBHOOK ---
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = telebot.types.Update.de_json(request.get_data().decode("utf-8"))
    bot.process_new_updates([update])
    return "OK", 200

@app.route("/")
def home():
    return "PixelinaBot está activo en Render 🚀"

# --- ARRANQUE DEL SERVIDOR ---
if __name__ == "__main__":
    bot.remove_webhook()
    render_url = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
    webhook_url = f"https://{render_url}/{TOKEN}"
    bot.set_webhook(url=webhook_url)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

