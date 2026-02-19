import os
import random
import telebot
from flask import Flask, request

# -------------------------------
# TOKEN seguro desde variable de entorno
TOKEN = os.environ.get("PIXELINA_TOKEN")
if not TOKEN:
    raise ValueError("❌ No se encontró PIXELINA_TOKEN en las variables de entorno de Render")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# -------------------------------
# MENÚ PRINCIPAL
def main_menu():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("📶 WiFi Escolar", "📚 Tareas")
    markup.row("👨‍🏫 ¿Dónde está el profe?", "🔮 Oráculo Tecno")
    markup.row("💡 Sugerencias", "🆘 Ayuda")
    markup.row("🗓 Calendario", "📣 Novedades", "💻 Proyectos")
    return markup

# -------------------------------
# RESPUESTAS DIVERTIDAS
wifi_msgs = [
    "¡No es tu compu! El WiFi del cole está tomando mate ☕",
    "Red inestable… alguien desconectó los cables para jugar a la escondida 🕵️‍♂️",
    "¡Ups! El WiFi se fue de recreo 🏃💨",
    "Pixelina recomienda reiniciar la compu y rezar 🙏💻"
]

tareas_msgs = [
    "¿Tenés tareas pendientes? ¡A por ellas! 📘💪",
    "Recordá anotar las tareas en la libreta digital 📓✨",
    "¡Nada de Netflix antes de entregar! 🍿🚫",
    "Hora de brillar con tus tareas 🌟"
]

profe_msgs = [
    "Está en la sala de profesores 📋, con cara de misterio 🤨",
    "¡Fue al kiosco! 😄 Probá ir con monedas 🪙",
    "Lo vi en el laboratorio 👨‍🔬 mezclando cosas raras 🧪",
    "Probablemente perdido en el pasillo 3… cuidado con los trolls 🧌"
]

oraculo_msgs = [
    "Hoy aprenderás algo nuevo sobre IA 🤖",
    "¡Tu código va a compilar sin errores! 💻",
    "Un bug oculto aparecerá en tu proyecto 👻",
    "Recibirás una gran idea para tu maqueta escolar 🧠",
    "Alguien te pedirá ayuda para colaborar 🤫",
    "Tu USB cobrará vida y bailará 🎵🖥️",
    "El próximo PowerPoint será tan épico que merecerá Oscar 🏆",
    "Cuidado con los stickers en el chat… podrían rebelarse 🐱‍👤",
    "Hoy es un buen día para encontrar la fórmula secreta del café ☕✨",
    "Alguien intentará hackear tu proyecto… ¡con amor! ❤️💾"
]

novedades_msgs = [
    "🆕 ¡Se viene un torneo de robótica! 🤖 Pronto más info.",
    "🎉 Hoy hay feria de ciencias, no te lo pierdas!",
    "📢 Recordá entregar tu trabajo de arte antes del viernes."
]

proyectos_msgs = [
    "🚀 PixelinaBot: maquetas automatizadas, apps y más. ¡Sumate! 🤩",
    "💡 Proyectos creativos: ¿tu idea será la próxima innovación?",
    "🛠️ Taller de inventos: hoy es un buen día para experimentar."
]

# -------------------------------
# HANDLER /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "👋 ¡Hola! Soy *PixelinaBot*, tu asistente escolar 🤖.\n"
        "Estoy lista para ayudarte con tareas, proyectos y dudas. "
        "Elegí una opción del menú 👇",
        parse_mode="Markdown",
        reply_markup=main_menu()
    )

# -------------------------------
# SALUDOS AUTOMÁTICOS
greetings = ["hola", "buen día", "buenos días", "buenas", "hey", "hi", "hello"]

@bot.message_handler(func=lambda m: any(greet in m.text.lower() for greet in greetings))
def saludo(message):
    saludos_respuestas = [
        "¡Hola! 👋 ¿Cómo andás?",
        "¡Hey! Listo para aprender algo nuevo hoy? 🤓",
        "¡Hola hola! PixelinaBot a tu servicio 🤖",
        "¡Buen día! ☀️ ¿Qué hacemos hoy?"
    ]
    bot.send_message(message.chat.id, random.choice(saludos_respuestas), reply_markup=main_menu())

# -------------------------------
# HANDLER DE MENSAJES (menú y demás)
@bot.message_handler(func=lambda m: True)
def responder_mensajes(message):
    txt = message.text.lower()
    print("Mensaje recibido:", txt)  # útil para depuración

    if txt in ["📶 wifi escolar", "wifi"]:
        bot.send_message(message.chat.id, random.choice(wifi_msgs))
    elif txt in ["📚 tareas", "tareas"]:
        bot.send_message(message.chat.id, random.choice(tareas_msgs))
    elif txt in ["👨‍🏫 ¿dónde está el profe?", "donde esta el profe"]:
        bot.send_message(message.chat.id, random.choice(profe_msgs))
    elif txt in ["🔮 oráculo tecno", "oraculo"]:
        bot.send_message(message.chat.id, random.choice(oraculo_msgs))
    elif txt in ["💡 sugerencias", "sugerencia"]:
        msg = bot.send_message(message.chat.id, "✍️ Escribí tu sugerencia, ¡yo la guardo!")
        bot.register_next_step_handler(msg, guardar_sugerencia)
    elif txt in ["🆘 ayuda", "ayuda"]:
        msg = bot.send_message(message.chat.id, "📨 Escribí tu consulta y alguien del equipo la verá.")
        bot.register_next_step_handler(msg, guardar_consulta)
    elif txt in ["🗓 calendario", "calendario"]:
        bot.send_message(message.chat.id, "📅 Próxima entrega: viernes 19/07.\n⚙️ Reunión de proyecto: lunes 22.")
    elif txt in ["📣 novedades", "novedades"]:
        bot.send_message(message.chat.id, random.choice(novedades_msgs))
    elif txt in ["💻 proyectos", "proyectos"]:
        bot.send_message(message.chat.id, random.choice(proyectos_msgs))
    elif txt in ["chau", "chao", "adios", "me voy"]:
        bot.send_message(message.chat.id, "👋 ¡Hasta pronto! PixelinaBot estará por acá cuando me necesites.")
    else:
        bot.send_message(message.chat.id, "No entendí eso 🤖. Probá con el menú 👇", reply_markup=main_menu())

# -------------------------------
# GUARDAR SUGERENCIAS Y CONSULTAS
def guardar_sugerencia(message):
    with open("sugerencias.txt", "a", encoding="utf-8") as f:
        f.write(f"{message.chat.id}: {message.text}\n")
    bot.send_message(message.chat.id, "¡Gracias! Tu sugerencia fue registrada.")

def guardar_consulta(message):
    with open("consultas.txt", "a", encoding="utf-8") as f:
        f.write(f"{message.chat.id}: {message.text}\n")
    bot.send_message(message.chat.id, "Tu mensaje fue enviado. ¡Gracias!")

# -------------------------------
# FLASK PARA WEBHOOK
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
    webhook_url = f"https://{render_url}/{TOKEN}"
    bot.set_webhook(url=webhook_url)
    print("✅ Webhook seteado en:", webhook_url)
else:
    print("❌ No se encontró RENDER_EXTERNAL_HOSTNAME. Revisá variables de entorno.")

# -------------------------------
# ARRANQUE DEL SERVIDOR
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
