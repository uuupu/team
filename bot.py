import requests
import time
import telebot
import os

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
bot = telebot.TeleBot(TOKEN)

coins = {
    "TON": "toncoin",
    "ETH": "ethereum",
    "SOL": "solana",
    "BTC": "bitcoin",
    "DOGE": "dogecoin",
    "PEPE": "pepe",
    "WIF": "dogwifcoin",
    "BONK": "bonk"
}

def get_price_change(coin_id):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}?localization=false&tickers=false&market_data=true&community_data=false&developer_data=false&sparkline=false"
    r = requests.get(url)
    data = r.json()
    price = data["market_data"]["current_price"]["usd"]
    change_24h = data["market_data"]["price_change_percentage_24h"]
    change_7d = data["market_data"]["price_change_percentage_7d"]
    volume = data["market_data"]["total_volume"]["usd"]
    return price, change_24h, change_7d, volume

def analyze_coin(name, coin_id):
    price, change_24h, change_7d, volume = get_price_change(coin_id)

    trend = "صاعد" if change_24h > 0 else "هابط"
    risk = "منخفضة" if abs(change_24h) < 3 else "متوسطة" if abs(change_24h) < 7 else "عالية"
    suggestion = "راقب فقط" if abs(change_24h) < 1 else "فرصة شراء" if change_24h < -3 else "فرصة متابعة"
    target = round(price * 1.10, 2)
    stop_loss = round(price * 0.93, 2)
    tax = round(min(20, max(5, price * 0.01)), 2)

    msg = f"""
تحليل ذكي - {name}
السعر الحالي: {price}$
الاتجاه: {trend}
تغير 24 ساعة: {change_24h:.2f}%
تغير 7 أيام: {change_7d:.2f}%
حجم التداول: {volume:,.0f}$
التوصية: {suggestion}
الهدف المتوقع: {target}$
ستوب لوس: {stop_loss}$
نسبة المخاطرة: {risk}
الضريبة المتوقعة: {tax}$  
"""
    return msg

def main_loop():
    messages = []
    for name, coin_id in coins.items():
        try:
            messages.append(analyze_coin(name, coin_id))
            time.sleep(1)
        except:
            continue

    full_message = "\n".join(messages)
    bot.send_message(CHAT_ID, full_message, parse_mode='Markdown')

while True:
    try:
        main_loop()
        time.sleep(3600)
    except Exception as e:
        bot.send_message(CHAT_ID, f"فيه خطأ في البوت: {e}")
        time.sleep(600)
