import os
import random
import telebot
import csv
from datetime import datetime

# -------------------------------
# TOKEN
TOKEN = os.environ.get("PIXELINA_TOKEN")
if not TOKEN:
    raise ValueError("PIXELINA_TOKEN no definido")

bot = telebot.TeleBot(TOKEN)

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
# INFORMACIÓN Y MENSAJES
wifi_info = "📶 Red: ColegioPixelina\n🔑 Contraseña: Pixelina1234"

tareas_msgs = [
    "📘 ¡No te atrases! Hacé tus tareas pronto y con ganas 💪",
    "📝 Cuanto antes las hagas, mejor será tu día ✨"
]

profe_msgs = [
    "Está en la sala de profesores 📋 con cara de misterio 🤨",
    "¡Fue al kiosco! 😄 Probá ir con monedas 🪙",
    "Lo vi en el laboratorio 👨‍🔬 con bata y goggles 🥼"
]

oraculo_msgs = [
    "Hoy aprenderás algo nuevo sobre IA 🤖",
    "¡Tu código va a compilar sin errores! 💻",
    "Un bug oculto aparecerá en tu proyecto 👻",
    "Recibirás una gran idea para tu maqueta escolar 🧠"
]

novedades_msgs = [
    "🆕 Pronto tendremos habilitado más salones, el comedor y los laboratorios!"
]

proyectos_lista = [
    "🚀 Cooperativa Escolar Clementina 2.0",
    "🤖 Robótica",
    "📱 Apps"
]

# -------------------------------
# FUNCIÓN PARA GUARDAR EN CSV
def guardar_registro(nombre_archivo, data):
    with open(nombre_archivo, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(data)

# -------------------------------
# COMANDO START
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "👋 ¡Hola! Soy *PixelinaBot*, tu asistente escolar 🤖.\n"
        "Elegí una opción del menú 👇",
        parse_mode="Markdown",
        reply_markup=main_menu()
    )

# -------------------------------
# HANDLER PRINCIPAL
@bot.message_handler(func=lambda m: True)
def responder_mensajes(message):
    txt = message.text.lower()

    if "wifi" in txt:
        bot.send_message(message.chat.id, wifi_info)

    elif "tareas" in txt:
        bot.send_message(message.chat.id, random.choice(tareas_msgs))

    elif "profe" in txt:
        bot.send_message(message.chat.id, random.choice(profe_msgs))

    elif "oráculo" in txt or "oraculo" in txt:
        bot.send_message(message.chat.id, random.choice(oraculo_msgs))

    # ---------------- SUGERENCIAS ----------------
    elif "sugerencia" in txt:
        msg = bot.send_message(message.chat.id, "✍️ Escribí tu sugerencia y la guardaré.")
        bot.register_next_step_handler(msg, guardar_sugerencia)

    # ---------------- AYUDA ----------------
    elif "ayuda" in txt:
        msg = bot.send_message(message.chat.id, "📨 Escribí tu consulta y alguien del equipo te responderá.")
        bot.register_next_step_handler(msg, guardar_ayuda)

    # ---------------- CALENDARIO ----------------
    elif "calendario" in txt:
        calendario_msg = (
            "📅 Inicio de ciclo lectivo:\n"
            "• Ingresantes: 2 de marzo\n"
            "• Resto de los cursos: 9 de marzo"
        )
        bot.send_message(message.chat.id, calendario_msg)

    # ---------------- NOVEDADES ----------------
    elif "novedades" in txt:
        bot.send_message(message.chat.id, random.choice(novedades_msgs))

    # ---------------- PROYECTOS ----------------
    elif "proyectos" in txt:
        bot.send_message(
            message.chat.id,
            "📌 Proyectos actuales:\n" + "\n".join(proyectos_lista) +
            "\n\n💡 Tu idea será la próxima innovación!!!\nEscribila y la registraré."
        )
        bot.register_next_step_handler(message, guardar_proyecto)

    elif any(x in txt for x in ["chau","adios","me voy","chao"]):
        bot.send_message(message.chat.id, "👋 ¡Hasta pronto!")

    else:
        bot.send_message(message.chat.id, "No entendí eso 🤖. Probá con el menú 👇", reply_markup=main_menu())

# -------------------------------
# FUNCIONES QUE GUARDAN MENSAJES

def guardar_sugerencia(message):
    celular = message.from_user.id
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    guardar_registro("sugerencias.csv", [celular, message.text, fecha])
    bot.send_message(message.chat.id, "✅ Gracias, tu sugerencia fue guardada.", reply_markup=main_menu())

def guardar_ayuda(message):
    celular = message.from_user.id
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    guardar_registro("ayuda.csv", [celular, message.text, fecha])
    bot.send_message(message.chat.id, "✅ Tu consulta fue registrada. Pronto te responderán.", reply_markup=main_menu())

def guardar_proyecto(message):
    celular = message.from_user.id
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    guardar_registro("proyectos.csv", [celular, message.text, fecha])
    bot.send_message(message.chat.id, "🚀 ¡Tu idea fue registrada! Gracias por innovar.", reply_markup=main_menu())

# -------------------------------
# ARRANQUE
print("🤖 PixelinaBot corriendo...")
bot.infinity_polling()
