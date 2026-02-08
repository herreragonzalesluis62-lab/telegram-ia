from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import openai
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

memoria = {}

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    mensaje = update.message.text

    if user_id not in memoria:
        memoria[user_id] = []

    memoria[user_id].append({"role": "user", "content": mensaje})
    memoria[user_id] = memoria[user_id][-10:]

    respuesta = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Responde como mensajes de texto. Corto, natural y humano. Español."
            }
        ] + memoria[user_id]
    )

    texto = respuesta.choices[0].message.content
    memoria[user_id].append({"role": "assistant", "content": texto})

    await update.message.reply_text(texto)

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))

print("Bot activo")
app.run_polling()
