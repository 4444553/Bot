import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# 🔹 Reemplaza con tu token de BotFather
TOKEN = "7943301440:AAEA8NebaHpMMKLwAVGPI6_b7tm_wm0p3Ug"

# 🔹 Configurar logs para depuración
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# 🔹 Función para obtener datos del BIN
async def obtener_info_bin(bin_number):
    url = f"https://lookup.binlist.net/{bin_number}"
    headers = {"Accept-Version": "3"}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()

            banco = data.get("bank", {}).get("name", "❌ No disponible")
            pais_nombre = data.get("country", {}).get("name", "❌ No disponible")
            pais_codigo = data.get("country", {}).get("alpha2", "❓")
            tipo = data.get("type", "❌ No disponible")
            esquema = data.get("scheme", "❌ No disponible")

            return (
                f"💳 BIN: {bin_number}\n"
                f"🏦 Banco: {banco}\n"
                f"🌍 País: {pais_nombre} ({pais_codigo})\n"
                f"🔹 Tipo: {tipo}\n"
                f"🔸 Esquema: {esquema}"
            )
        elif response.status_code == 404:
            return "⚠️ BIN no encontrado en la base de datos."
        else:
            return f"⚠️ Error en la API ({response.status_code})."

    except requests.exceptions.RequestException as e:
        return f"❌ Error de conexión: {e}"

# 🔹 Función que maneja mensajes con BINs
async def manejar_mensaje(update: Update, context: CallbackContext):
    mensaje = update.message.text.strip()

    if mensaje.isdigit() and 6 <= len(mensaje) <= 8:
        info = await obtener_info_bin(mensaje)
        await update.message.reply_text(info)
    else:
        await update.message.reply_text("⚠️ Envía un BIN válido (6 a 8 dígitos).")

# 🔹 Comando /start
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "🤖 ¡Hola! Envíame un BIN (primeros 6-8 dígitos de una tarjeta) y te diré su información."
    )

# 🔹 Función principal
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, manejar_mensaje))

    print("✅ Bot en ejecución...")
    app.run_polling()

if __name__ == "__main__":
    main()
