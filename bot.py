import os
import requests
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

VALYUTALAR = ['USD', 'EUR', 'GBP', 'CNY', 'RUB']

def get_rates():
    resp = requests.get('https://api.exchangerate.host/latest', params={'base': 'UZS', 'symbols': ','.join(VALYUTALAR)})
    data = resp.json()
    return data['rates']

def start(update: Update, context: CallbackContext):
    menu = [['💱 Hozirgi kurs'], ['💰 Soʻm kiriting']]
    update.message.reply_text("Assalomu alaykum! Valyuta kurs botiga xush kelibsiz.", reply_markup=ReplyKeyboardMarkup(menu, resize_keyboard=True))

def handle_message(update: Update, context: CallbackContext):
    text = update.message.text.strip()
    rates = get_rates()
    if text == "💱 Hozirgi kurs":
        msg = "💱 1 soʻm bahosi:\n"
        for v in VALYUTALAR:
            kurs = rates.get(v)
            msg += f"{v}: {kurs:.6f}\n"
        update.message.reply_text(msg)
    elif text == "💰 Soʻm kiriting":
        update.message.reply_text("Iltimos, soʻm miqdorini raqamda kiriting:")
    elif text.replace('.', '', 1).isdigit():
        amount = float(text)
        msg = f"{int(amount)} soʻm quyidagicha:\n"
        for v in VALYUTALAR:
            kurs = rates.get(v)
            msg += f"{v}: {round(amount * kurs, 2)}\n"
        update.message.reply_text(msg)
    else:
        update.message.reply_text("Iltimos, menyudagi tugmalardan birini tanlang.")

def main():
    token = os.getenv("BOT_TOKEN")
    updater = Updater(token=token, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
