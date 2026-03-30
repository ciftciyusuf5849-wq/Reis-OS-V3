import os
import random
import requests
import asyncio
import nest_asyncio
from bs4 import BeautifulSoup
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# --- 7/24 UYANIK KALMA VE AKILLI PORT SİSTEMİ ---
app = Flask('')

@app.route('/')
def home():
    return "Reis-OS 7/24 Aktif ve Nöbette!"

def run():
    # Render'ın verdiği kapıyı (port) otomatik çekiyoruz
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- HAYALET MODU İNTERNET AVCI FONKSİYONU ---
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36"
]

def internette_avlan(sorgu):
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    url = f"https://www.google.com/search?q={sorgu}&hl=tr"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            snippets = soup.find_all("div", class_="VwiC3b") 
            sonuc = "\n\n".join([s.get_text() for s in snippets[:3]])
            return sonuc if sonuc else "Bilgiye ulaşıldı ama analiz edilemedi reisim."
        return "Google kapıyı kapattı, sızamadım."
    except:
        return "Bağlantı koptu reisim."

# --- TELEGRAM BOT KOMUTLARI ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Reis-OS v3 Çelik Gibi Aktif! Emret reisim.")

async def cevapla(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    await update.message.reply_text("🔍 Bilgi avlanıyor, beklemedeyiz...")
    bilgi = internette_avlan(user_msg)
    await update.message.reply_text(f"🛡️ **Bilgi Merkezi** 🛡️\n\n{bilgi}")

# --- ANA ÇALIŞTIRICI ---
if __name__ == '__main__':
    keep_alive() # Portu otomatik ayarlayıp webi başlatır
    
    # TOKENİ BURAYA YAPIŞTIRMAYI UNUTMA REİSİM
    TOKEN = "8793626803:AAGRuqr-43_re2L0XjLdup3jda5I3WjD6ac"
    
    nest_asyncio.apply()
    app_telegram = ApplicationBuilder().token(TOKEN).build()
    app_telegram.add_handler(CommandHandler("start", start))
    app_telegram.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), cevapla))
    
    app_telegram.run_polling()



