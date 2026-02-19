# -------------------------------
# HANDLERS
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

    # ---------------- SUGERENCIAS ----------------
    elif "sugerencia" in txt or "💡" in txt:
        msg = bot.send_message(message.chat.id, "✍️ Escribí tu sugerencia y la guardaré.")
        bot.register_next_step_handler(msg, guardar_sugerencia)

    # ---------------- AYUDA ----------------
    elif "ayuda" in txt or "🆘" in txt:
        msg = bot.send_message(message.chat.id, "📨 Escribí tu consulta y alguien del equipo te responderá.")
        bot.register_next_step_handler(msg, guardar_ayuda)

    # ---------------- CALENDARIO ----------------
    elif "calendario" in txt or "🗓" in txt:
        calendario_msg = (
            "📅 Inicio de ciclo lectivo:\n"
            "- Ingresantes: 2 de marzo\n"
            "- Resto de los cursos: 9 de marzo"
        )
        bot.send_message(message.chat.id, calendario_msg)

    # ---------------- NOVEDADES ----------------
    elif "novedades" in txt or "📣" in txt:
        bot.send_message(message.chat.id, random.choice(novedades_msgs))

    # ---------------- PROYECTOS ----------------
    elif "proyectos" in txt or "💻" in txt:
        bot.send_message(message.chat.id, "📌 Proyectos actuales:\n" + "\n".join(proyectos_msgs))
        msg = bot.send_message(message.chat.id, "💡 Podés escribir tu idea y quedará registrada.")
        bot.register_next_step_handler(msg, guardar_proyecto)

    # ---------------- SALUDOS / DESPEDIDAS ----------------
    elif any(x in txt for x in ["chau","adios","me voy","chao"]):
        bot.send_message(message.chat.id, "👋 ¡Hasta pronto! PixelinaBot estará por acá cuando me necesites.")
    else:
        bot.send_message(message.chat.id, "No entendí eso 🤖. Probá con el menú 👇", reply_markup=main_menu())

# -------------------------------
# FUNCIONES DE GUARDADO
def guardar_sugerencia(message):
    celular = message.from_user.id
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    guardar_registro("sugerencias.csv", [celular, message.text, fecha])
    bot.send_message(message.chat.id, "✅ Gracias, tu sugerencia fue guardada.", reply_markup=main_menu())

def guardar_ayuda(message):
    celular = message.from_user.id
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    guardar_registro("ayuda.csv", [celular, message.text, fecha])
    bot.send_message(message.chat.id, "✅ Tu consulta fue registrada. Alguien del equipo te responderá pronto.", reply_markup=main_menu())

def guardar_proyecto(message):
    celular = message.from_user.id
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    guardar_registro("proyectos.csv", [celular, message.text, fecha])
    bot.send_message(message.chat.id, "✅ Tu idea fue registrada. ¡Gracias por compartirla!", reply_markup=main_menu())
