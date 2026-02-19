import os
import random
import telebot
import csv
from datetime import datetime

# -------------------------------
# TOKEN desde variable de entorno
TOKEN = os.environ.get("PIXELINA_TOKEN")
if not TOKEN:
    raise ValueError("PIXELINA_TOKEN no definido en variables de entorno")

bot = telebot.TeleBot(TOKEN)

# -------------------------------
# ⚠️ Eliminar webhook antiguo para evitar conflictos 409
bot.remove_webhook()
print("✅ Webhook eliminado, listo para polling")

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
# RESPUESTAS DIVERTIDAS / INFO
wifi_info = "Red: ColegioPixelina\nContraseña: Pixelina1234"
tareas_msgs = [
    "¡No te atrases! 📘 Hacé tus tareas pronto y con ganas 💪",
    "Recordá: cuanto antes las hagas, mejor será tu día 📝✨"
]
profe_msgs = [
    "Está en la sala de profesores  🤨",
    "¡Fue al kiosco! 😄  🪙",
    "Lo vi en la biblioteca🥼"
]
oraculo_msgs = [
    "Hoy aprenderás algo nuevo sobre IA 🤖",
    "¡Tu código va a compilar sin errores! 💻",
    "Un bug oculto aparecerá en tu proyecto 👻",
    "Recibirás una gran idea para tu maqueta escolar 🧠",
    "Alguien intentará hackear tu proyecto… ¡con amor! ❤️💾",
    "Tu USB cobrará vida y bailará 🎵🖥️",
    "El próximo PowerPoint será tan épico que merecerá un Oscar 🏆",
    "Cuidado con los stickers en el chat… podrían rebelarse 🐱‍👤",
    "Hoy es un buen día para encontrar la fórmula secreta de cómo cebar un buen mate ☕✨",
    "Tu proyecto tendrá un aliado misterioso 😎",
    "Un compañero te sorprenderá con un dato curioso 🧩"
]
novedades_msgs = [
    "🆕 Pronto tendremos habilitado más salones, el comedor y los laboratorios!"
]
proyectos_msgs = [
    "🚀 Cooperativa Escolar Clementina 2.0",
    "🤖 Robótica",
    "💡 Apps y tu idea será la próxima innovación!!!"
]

# -------------------------------
# SALUDOS AUTOMÁTICOS
greetings = ["hola", "buen día", "buenos días", "buenas", "hey", "hi", "hello"]

# -------------------------------
# FUNCIONES DE REGISTRO
def guardar_registro(nombre_archivo, data):
    # data = [celular, mensaje, fecha]
    with open(nombre_archivo, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(data)

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
    celular = message.from_user.id
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if "wifi" in txt:
        bot.send_message(message.chat.id, wifi_info)
    elif "tareas" in txt:
        bot.send_message(message.chat.id, random.choice(tareas_msgs))
    elif "profe" in txt:
        bot.send_message(message.chat.id, random.choice(profe_msgs))
    elif "oráculo" in txt or "oraculo" in txt:
        bot.send_message(message.chat.id, random.choice(oraculo_msgs))
    elif "sugerencia" in txt or "💡" in txt:
        bot.send_message(message.chat.id, "✍️ Gracias! Tu sugerencia fue registrada.")
        guardar_registro("sugerencias.csv", [celular, message.text, fecha])
    elif "ayuda" in txt or "🆘" in txt:
        bot.send_message(message.chat.id, "📨 Tu consulta fue registrada. Alguien del equipo responderá pronto.")
        guardar_registro("ayuda.csv", [celular, message.text, fecha])
    elif "calendario" in txt or "🗓" in txt:
        calendario_msg = (
            "📅 Inicio de ciclo lectivo:\n"
            "- Ingresantes: 2 de marzo\n"
            "- Resto de los cursos: 9 de marzo"
        )
        bot.send_message(message.chat.id, calendario_msg)
    elif "novedades" in txt or "📣" in txt:
        bot.send_message(message.chat.id, random.choice(novedades_msgs))
    elif "proyectos" in txt or "💻" in txt:
        bot.send_message(message.chat.id, "📌 Proyectos actuales:\n" + "\n".join(proyectos_msgs))
        bot.send_message(message.chat.id, "💡 Podés escribir tu idea y quedará registrada.")
        # Guardar si el mensaje es la idea
        if message.text not in proyectos_msgs:
            guardar_registro("proyectos.csv", [celular, message.text, fecha])
    elif any(x in txt for x in ["chau","adios","me voy","chao"]):
        bot.send_message(message.chat.id, "👋 ¡Hasta pronto! PixelinaBot estará por acá cuando me necesites.")
    else:
        bot.send_message(message.chat.id, "No entendí eso 🤖. Probá con el menú 👇", reply_markup=main_menu())

# -------------------------------
# ARRANQUE CON POLLING
print("PixelinaBot corriendo con polling…")
bot.infinity_polling()
