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
    data = response.json()
    
    if 'price' in data:
        return float(data['price'])
    else:
        return None  # Algo salió mal

def send_telegram_message(bot, message):
    bot.send_message(chat_id=CHAT_ID, text=message)

bot = Bot(token=TELEGRAM_TOKEN)

def job():
    price = get_eth_price()
    if price:
        message = f"💰 El precio actual de ETH/USDT es: {price} USD"
    else:
        message = "⚠️ Error al obtener el precio de ETH. Binance no respondió correctamente."
    send_telegram_message(bot, message)

schedule.every(1).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
