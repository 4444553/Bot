from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import logging
import re
from faker import Faker

# Configurar logging
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

# Token del bot de Telegram (reemplázalo con tu token real)
TOKEN = "8090451672:AAGrJrUNfHfPjrcIQiJCo5pY0Lz5fgmkEdE"

# Mapeo de nombres de países a códigos de Faker
PAISES_FAKER = {
    "españa": "es_ES", "francia": "fr_FR", "alemania": "de_DE", "italia": "it_IT", "estados unidos": "en_US",
    "reino unido": "en_GB", "méxico": "es_MX", "brasil": "pt_BR", "argentina": "es_AR", "canadá": "en_CA",
    "portugal": "pt_PT", "japón": "ja_JP", "china": "zh_CN", "rusia": "ru_RU", "india": "hi_IN",
    "países bajos": "nl_NL", "suecia": "sv_SE", "noruega": "no_NO", "finlandia": "fi_FI", "polonia": "pl_PL",
    "suiza": "de_CH", "australia": "en_AU", "nueva zelanda": "en_NZ", "grecia": "el_GR", "corea del sur": "ko_KR",
    "turquía": "tr_TR", "sudáfrica": "en_ZA", "ucrania": "uk_UA", "emiratos árabes": "ar_AE", "egipto": "ar_EG",
    "venezuela": "es_VE", "colombia": "es_CO", "chile": "es_CL", "perú": "es_PE", "ecuador": "es_EC",
    "bolivia": "es_BO", "paraguay": "es_PY", "uruguay": "es_UY", "honduras": "es_HN", "cuba": "es_CU",
    "dominicana": "es_DO", "guatemala": "es_GT", "costa rica": "es_CR", "panamá": "es_PA", "filipinas": "tl_PH",
    "malasia": "ms_MY", "indonesia": "id_ID", "tailandia": "th_TH", "vietnam": "vi_VN", "pakistán": "ur_PK",
    "bangladés": "bn_BD", "arabia saudita": "ar_SA", "israel": "he_IL", "irán": "fa_IR", "kazajistán": "kk_KZ",
    "uzbekistán": "uz_UZ", "mongolia": "mn_MN", "nigeria": "en_NG", "kenia": "en_KE", "ghana": "en_GH",
    "tanzania": "sw_TZ", "argelia": "ar_DZ", "maruecos": "fr_MA", "senegal": "fr_SN", "etiopía": "am_ET",
    "el salvador": "es_SV", "nicaragua": "es_NI", "puerto rico": "es_PR"
}

def generar_datos_falsos(pais: str):
    pais = pais.lower()
    if pais in PAISES_FAKER:
        fake = Faker(PAISES_FAKER[pais])
        datos = (
            "\n"
            "------------------------------\n"
            f"📌 *Datos Generados para {pais.capitalize()}*\n"
            "------------------------------\n"
            f"👤 *Nombre:* `{fake.name()}`\n"
            f"🏠 *Dirección:* \n`{fake.address().replace('-', r'\-')}`\n"  # Escapa guiones
            f"📧 *Correo:* `{fake.email()}`\n"
            f"📞 *Teléfono:* `{fake.phone_number()}`\n"
            f"🎂 *Fecha de Nacimiento:* `{fake.date_of_birth(minimum_age=18, maximum_age=70)}`\n"
            "------------------------------"
        )
        return datos
    else:
        return "⚠️ *País no soportado.* Intenta con un país válido."

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("¡Hola! Escribe el nombre de un país para generar datos.")

async def generate_fake_data(update: Update, context: CallbackContext) -> None:
    text = update.message.text.lower()
    resultado = generar_datos_falsos(text)
    await update.message.reply_text(resultado, parse_mode="MarkdownV2")

def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_fake_data))
    
    print("🤖 Bot en marcha... Presiona Ctrl + C para detenerlo.")
    app.run_polling()

if __name__ == "__main__":
    main()
