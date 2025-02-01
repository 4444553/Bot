from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import logging
import re
from faker import Faker

# Configurar logging
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

# Token del bot de Telegram (reemplázalo con tu token real)
TOKEN = "7858840568:AAHyJRlMuznwkXkQw-9Kn6MbPNjDvPqa4ow"

# Mapeo de nombres de países a códigos de Faker
PAISES_FAKER = {
    "venezuela": "es_VE", "españa": "es_ES", "francia": "fr_FR", "alemania": "de_DE", "italia": "it_IT",
    "estados unidos": "en_US", "reino unido": "en_GB", "méxico": "es_MX", "brasil": "pt_BR",
    "argentina": "es_AR", "canadá": "en_CA", "portugal": "pt_PT", "japón": "ja_JP", "china": "zh_CN",
    "rusia": "ru_RU", "india": "hi_IN", "países bajos": "nl_NL", "suecia": "sv_SE", "noruega": "no_NO",
    "finlandia": "fi_FI", "polonia": "pl_PL", "suiza": "de_CH", "australia": "en_AU", "nueva zelanda": "en_NZ",
    "grecia": "el_GR", "corea del sur": "ko_KR", "turquía": "tr_TR", "sudáfrica": "en_ZA", "ucrania": "uk_UA",
    "colombia": "es_CO", "chile": "es_CL", "perú": "es_PE", "ecuador": "es_EC", "bolivia": "es_BO",
    "paraguay": "es_PY", "uruguay": "es_UY", "honduras": "es_HN", "cuba": "es_CU", "dominicana": "es_DO",
    "guatemala": "es_GT", "costa rica": "es_CR", "panamá": "es_PA", "filipinas": "tl_PH", "malasia": "ms_MY",
    "indonesia": "id_ID", "tailandia": "th_TH", "vietnam": "vi_VN", "pakistán": "ur_PK", "bangladés": "bn_BD",
    "arabia saudita": "ar_SA", "israel": "he_IL", "irán": "fa_IR", "kazajistán": "kk_KZ", "uzbekistán": "uz_UZ",
    "mongolia": "mn_MN", "nigeria": "en_NG", "kenia": "en_KE", "ghana": "en_GH", "tanzania": "sw_TZ",
    "argelia": "ar_DZ", "marruecos": "fr_MA", "senegal": "fr_SN", "etiopía": "am_ET", "el salvador": "es_SV",
    "nicaragua": "es_NI", "puerto rico": "es_PR"
}

def escape_markdown_v2(text):
    """Escapa caracteres especiales de Markdown v2."""
    special_chars = r"[_*[]()~`>#+-=|{}.!\\]"
    return re.sub(f'([{special_chars}])', r'\\\1', text) if isinstance(text, str) else str(text)

def generar_datos_falsos(pais: str):
    """Genera datos falsos según el país dado."""
    pais = pais.lower()
    if pais in PAISES_FAKER:
        fake = Faker(PAISES_FAKER[pais])
        try:
            codigo_postal = escape_markdown_v2(fake.postcode())  # Se usa postcode() para mayor compatibilidad
        except AttributeError:
            codigo_postal = "No disponible"

        datos = (
            f"\U0001F4CC *DATOS PARA: {pais.capitalize()}* \n\n"
            f"\U0001F464 *NOMBRE:* `{escape_markdown_v2(fake.name())}`\n"
            f"\U0001F3E0 *DIRECCIÓN:* `{escape_markdown_v2(fake.street_address())}`\n"  # Direcciones más cortas
            f"\U0001F4E7 *CORREO:* `{escape_markdown_v2(fake.email())}`\n"
            f"\U0001F4DE *TELÉFONO:* `{escape_markdown_v2(fake.phone_number())}`\n"
            f"\U0001F382 *NACIMIENTO:* `{escape_markdown_v2(fake.date_of_birth(minimum_age=18, maximum_age=70).strftime('%Y-%m-%d'))}`\n"
            f"\U0001F4CD *CÓDIGO POSTAL:* `{codigo_postal}`\n"
        )
        return datos
    else:
        return "⚠️ *País no soportado.* Intenta con un país válido."

async def start(update: Update, context: CallbackContext) -> None:
    """Mensaje de bienvenida."""
    await update.message.reply_text("¡Hola! Usa `/tok [país]` en grupos o envía el nombre del país en el chat privado.")

async def generate_fake_data(update: Update, context: CallbackContext) -> None:
    """Genera datos en chat privado sin necesidad del comando."""
    if update.message.chat.type == "private":
        text = update.message.text.lower()
        resultado = generar_datos_falsos(text)
        await update.message.reply_text(resultado, parse_mode="MarkdownV2")

async def generate_fake_data_from_command(update: Update, context: CallbackContext) -> None:
    """Genera datos en grupos cuando se usa el comando /tok."""
    if context.args:
        pais = " ".join(context.args).lower()
        resultado = generar_datos_falsos(pais)
        await update.message.reply_text(resultado, parse_mode="MarkdownV2")
    else:
        await update.message.reply_text("❌ Debes escribir un país después de /tok. Ejemplo: `/tok España`", parse_mode="MarkdownV2")

def main():
    app = Application.builder().token(TOKEN).build()
    
    # Manejar comandos y mensajes
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("tok", generate_fake_data_from_command))  # Solo responde en grupos con /tok
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_fake_data))  # En privado solo manda el país

    print("🤖 Bot en marcha... Presiona Ctrl + C para detenerlo.")
    app.run_polling()

if __name__ == "__main__":
    main()
