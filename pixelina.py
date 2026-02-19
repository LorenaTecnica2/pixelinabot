import telebot
import os
import csv
import random
from datetime import datetime
from telebot.types import ReplyKeyboardMarkup

# -------------------------------
# TOKEN DESDE RENDER
TOKEN = os.environ.get("PIXELINA_TOKEN")
if not TOKEN:
    raise ValueError("PIXELINA_TOKEN no definido")

bot = telebot.TeleBot(TOKEN)

# 🔐 PONÉ TU ID REAL ACÁ
ADMIN_ID = 1551887836

bot.remove_webhook()
print("✅ Bot iniciado en modo polling")

# -------------------------------
# TEXTOS

wifi_info = "📶 Red: Pixelina\n🔑 Contraseña: pixelina123"

tareas_msgs = [
    "📚 Recordá entregar la tarea mañana.",
    "📝 No olvides revisar Classroom."
]

profe_msgs = [
    "👩‍🏫 La profe responde en horario escolar.",
    "📧 También podés escribirle por mail."
]

oraculo_msgs = [
    "🔮 Hoy será un gran día.",
    "✨ Confía en tu intuición."
]

novedades_msgs = [
    "📣 Nueva actividad esta semana.",
    "🎉 Se viene un evento especial."
]

proyectos_msgs = [
    "💻 App educativa",
    "🤖 Robot escolar",
    "🌱 Proyecto ambiental"
]

# -------------------------------
# MENÚ PRINCIPAL

def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("📶 Wifi", "📚 Tareas")
    markup.row("👩‍🏫 Profe", "🔮 Oráculo")
    markup.row("💡 Sugerencia", "🆘 Ayuda")
    markup.row("🗓 Calendario", "📣 Novedades")
    markup.row("💻 Proyectos")
    return markup

# -------------------------------
# FUNCIÓN PARA GUARDAR CSV

def guardar_registro(archivo, datos):
    existe = os.path.isfile(archivo)

    with open(archivo, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if not existe:
            writer.writerow(["usuario_id", "mensaje", "fecha"])

        writer.writerow(datos)

# -------------------------------
# START

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "👋 Hola, soy PixelinaBot 🤖\nElegí una opción del menú:",
        reply_markup=main_menu()
    )

# -------------------------------
# HANDLER GENERAL

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

    elif "sugerencia" in txt:
        msg = bot.send_message(message.chat.id, "✍️ Escribí tu sugerencia y la guardaré.")
        bot.register_next_step_handler(msg, guardar_sugerencia)

    elif "ayuda" in txt:
        msg = bot.send_message(message.chat.id, "📨 Escribí tu consulta y alguien del equipo te responderá.")
        bot.register_next_step_handler(msg, guardar_ayuda)

    elif "calendario" in txt:
        calendario_msg = (
            "📅 Inicio de ciclo lectivo:\n"
            "- Ingresantes: 2 de marzo\n"
            "- Resto: 9 de marzo"
        )
        bot.send_message(message.chat.id, calendario_msg)

    elif "novedades" in txt:
        bot.send_message(message.chat.id, random.choice(novedades_msgs))

    elif "proyectos" in txt:
        bot.send_message(message.chat.id, "📌 Proyectos actuales:\n" + "\n".join(proyectos_msgs))
        msg = bot.send_message(message.chat.id, "💡 Podés escribir tu idea y quedará registrada.")
        bot.register_next_step_handler(msg, guardar_proyecto)

    elif any(x in txt for x in ["chau","adios","me voy"]):
        bot.send_message(message.chat.id, "👋 ¡Hasta pronto!", reply_markup=main_menu())

    else:
        bot.send_message(message.chat.id, "No entendí eso 🤖. Probá con el menú 👇", reply_markup=main_menu())

# -------------------------------
# FUNCIONES DE GUARDADO

def guardar_sugerencia(message):
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    guardar_registro("sugerencias.csv", [message.from_user.id, message.text, fecha])

    bot.send_message(
        ADMIN_ID,
        f"📩 NUEVA SUGERENCIA\n\n👤 {message.from_user.id}\n📝 {message.text}\n📅 {fecha}"
    )

    bot.send_message(message.chat.id, "✅ Gracias, tu sugerencia fue guardada.", reply_markup=main_menu())

def guardar_ayuda(message):
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    guardar_registro("ayuda.csv", [message.from_user.id, message.text, fecha])

    bot.send_message(
        ADMIN_ID,
        f"🆘 NUEVA CONSULTA\n\n👤 {message.from_user.id}\n📝 {message.text}\n📅 {fecha}"
    )

    bot.send_message(message.chat.id, "✅ Tu consulta fue registrada.", reply_markup=main_menu())

def guardar_proyecto(message):
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    guardar_registro("proyectos.csv", [message.from_user.id, message.text, fecha])

    bot.send_message(
        ADMIN_ID,
        f"💻 NUEVA IDEA\n\n👤 {message.from_user.id}\n📝 {message.text}\n📅 {fecha}"
    )

    bot.send_message(message.chat.id, "✅ Tu idea fue registrada.", reply_markup=main_menu())

# -------------------------------
# ADMIN RESPONDER Y GUARDAR

@bot.message_handler(commands=['responder'])
def responder_usuario(message):
    if message.from_user.id != ADMIN_ID:
        return

    try:
        partes = message.text.split(" ", 2)

        if len(partes) < 3:
            bot.send_message(message.chat.id, "Formato correcto:\n/responder ID mensaje")
            return

        user_id = int(partes[1])
        respuesta = partes[2]
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        bot.send_message(user_id, f"📩 Respuesta del equipo:\n\n{respuesta}")
        guardar_registro("respuestas.csv", [user_id, respuesta, fecha])

        bot.send_message(message.chat.id, "✅ Respuesta enviada y guardada.")

    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {e}")

# -------------------------------
# VER ÚLTIMOS REGISTROS

@bot.message_handler(commands=['ver'])
def ver_csv(message):
    if message.from_user.id != ADMIN_ID:
        return

    partes = message.text.split(" ")
    if len(partes) < 2:
        bot.send_message(message.chat.id, "Usá:\n/ver sugerencias\n/ver ayuda\n/ver proyectos\n/ver respuestas")
        return

    archivo = partes[1].lower() + ".csv"

    if not os.path.exists(archivo):
        bot.send_message(message.chat.id, "Ese archivo no existe.")
        return

    with open(archivo, "r", encoding="utf-8") as f:
        lineas = f.readlines()

    if len(lineas) <= 1:
        bot.send_message(message.chat.id, "No hay registros todavía.")
        return

    ultimas = lineas[-10:]
    texto = f"📂 Últimos registros de {archivo}:\n\n" + "".join(ultimas)

    bot.send_message(message.chat.id, texto[:4000])

# -------------------------------
# DESCARGAR CSV

@bot.message_handler(commands=['descargar'])
def descargar_csv(message):
    if message.from_user.id != ADMIN_ID:
        return

    partes = message.text.split(" ")
    if len(partes) < 2:
        bot.send_message(message.chat.id, "Usá:\n/descargar sugerencias\n/descargar ayuda\n/descargar proyectos\n/descargar respuestas")
        return

    archivo = partes[1].lower() + ".csv"

    if not os.path.exists(archivo):
        bot.send_message(message.chat.id, "Ese archivo no existe.")
        return

    with open(archivo, "rb") as f:
        bot.send_document(message.chat.id, f)

# -------------------------------
# INICIAR BOT

bot.infinity_polling()
