import requests
import time
from telegram import Bot
import schedule
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def get_eth_price():
    url = "https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT"
    try:
        response = requests.get(url)
        data = response.json()
        print("📦 Respuesta completa de Binance:", data)  # 🔍 LOG explícito
    except Exception as e:
        print("❌ Error al hacer request o parsear JSON:", e)
        return None

    if 'price' in data:
        return float(data['price'])
    else:
        return None

def send_telegram_message(bot, message):
    bot.send_message(chat_id=CHAT_ID, text=message)

bot = Bot(token=TELEGRAM_TOKEN)

def job():
    print("🔁 Ejecutando job()")  # Confirmación visual
    price = get_eth_price()
    if price:
        message = f"💰 El precio actual de ETH/USDT es: {price} USD"
    else:
        message = "⚠️ No se pudo obtener el precio de ETH. Revisá los logs de Binance."
    send_telegram_message(bot, message)

# Forzar un mensaje inmediato para ver los logs ahora
job()

# Y seguir cada hora
schedule.every().hour.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
