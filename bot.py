import requests
import time
from telegram import Bot
import schedule
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def get_eth_price():
    url = "https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT"
    response = requests.get(url)
    try:
        data = response.json()
    except Exception as e:
        print(f"❌ Error al parsear respuesta de Binance: {e}")
        return None

    if 'price' in data:
        return float(data['price'])
    else:
        print("❌ Binance devolvió:", data)
        return None

def send_telegram_message(bot, message):
    bot.send_message(chat_id=CHAT_ID, text=message)

bot = Bot(token=TELEGRAM_TOKEN)

def job():
    price = get_eth_price()
    if price:
        message = f"💰 El precio actual de ETH/USDT es: {price} USD"
    else:
        message = "⚠️ No se pudo obtener el precio de ETH. Revisá los logs de Binance."
    send_telegram_message(bot, message)

# ⏱️ Ejecutar cada 1 hora
schedule.every().hour.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
