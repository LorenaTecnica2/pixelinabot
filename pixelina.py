import os
import random
import telebot

# -------------------------------
# TOKEN desde variable de entorno
TOKEN = os.environ.get("PIXELINA_TOKEN")
if not TOKEN:
    raise ValueError("PIXELINA_TOKEN no definido en variables de entorno")

bot = telebot.TeleBot(TOKEN)

# -------------------------------
# ⚠️ ELIMINAR WEBHOOK Y asegurar polling único
bot.remove_webhook()
print("✅ Webhook eliminado, listo para polling")
print("✅ Asegurate de que no haya otra instancia de PixelinaBot corriendo")

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
    "¡Ups! El WiFi se fue de recreo 🏃💨"
]

tareas_msgs = [
    "¿Tenés tareas pendientes? ¡A por ellas! 📘💪",
    "Recordá anotar las tareas en la libreta digital 📓✨"
]

profe_msgs = [
    "Está en la sala de profesores 📋, con cara de misterio 🤨",
    "¡Fue al kiosco! 😄 Probá ir con monedas 🪙"
]

oraculo_msgs = [
    "Hoy aprenderás algo nuevo sobre IA 🤖",
    "¡Tu código va a compilar sin errores! 💻",
    "Un bug oculto aparecerá en tu proyecto 👻",
    "Recibirás una gran idea para tu maqueta escolar 🧠",
    "Alguien intentará hackear tu proyecto… ¡con amor! ❤️💾",
    "Tu USB cobrará vida y bailará 🎵🖥️",
    "El próximo PowerPoint será tan épico que merecerá Oscar 🏆",
    "Cuidado con los stickers en el chat… podrían rebelarse 🐱‍👤",
    "Hoy es un buen día para encontrar la fórmula secreta del café ☕✨"
]

novedades_msgs = [
    "🆕 ¡Se viene un torneo de robótica! 🤖",
    "🎉 Hoy hay feria de ciencias, no te lo pierdas!",
    "📢 Recordá entregar tu trabajo de arte antes del viernes."
]

proyectos_msgs = [
    "🚀 PixelinaBot: maquetas automatizadas, apps y más. ¡Sumate! 🤩",
    "💡 Proyectos creativos: ¿tu idea será la próxima innovación?",
    "🛠️ Taller de inventos: hoy es un buen día para experimentar."
]

# -------------------------------
# SALUDOS AUTOMÁTICOS
greetings = ["hola", "buen día", "buenos días", "buenas", "hey", "hi", "hello"]

# -------------------------------
# HANDLERS
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "👋 ¡Hola! Soy *PixelinaBot*, tu asistente escolar 🤖.\n"
        "Estoy lista para ayudarte con tareas, proyectos y dudas. Elegí una opción del menú 👇",
        parse_mode="Markdown",
        reply_markup=main_menu()
    )

@bot.message_handler(func=lambda m: any(greet in m.text.lower() for greet in greetings))
def saludo(message):
    saludos_respuestas = [
        "¡Hola! 👋 ¿Cómo andás?",
        "¡Hey! Listo para aprender algo nuevo hoy? 🤓",
        "¡Hola hola! PixelinaBot a tu servicio 🤖",
        "¡Buen día! ☀️ ¿Qué hacemos hoy?"
    ]
    bot.send_message(message.chat.id, random.choice(saludos_respuestas), reply_markup=main_menu())

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
        bot.send_message(message.chat.id, random.choice(novedades_msgs))
    elif "proyectos" in txt or "💻" in txt:
        bot.send_message(message.chat.id, random.choice(proyectos_msgs))
    elif any(x in txt for x in ["chau","adios","me voy","chao"]):
        bot.send_message(message.chat.id, "👋 ¡Hasta pronto! PixelinaBot estará por acá cuando me necesites.")
    else:
        bot.send_message(message.chat.id, "No entendí eso 🤖. Probá con el menú 👇", reply_markup=main_menu())

# -------------------------------
# ARRANQUE CON POLLING
print("PixelinaBot corriendo con polling…")
bot.infinity_polling()
