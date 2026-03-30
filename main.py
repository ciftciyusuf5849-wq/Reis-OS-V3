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

# --- 7/24 UYANIK KALMA SİSTEMİ (KEEP-ALIVE) ---
app = Flask('')

@app.route('/')
def home():
    return "Reis-OS 7/24 Aktif ve Nöbette!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- HAYALET MODU İNTERNET AVCI FONKSİYONU ---
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36"
]

def internette_avlan(sorgu):
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    url = f"https://www.google.com/search?q={sorgu}&hl=tr"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            # Google'ın arama sonuç özetlerini (snippet) topluyoruz
            snippets = soup.find_all("div", class_="VwiC3b") 
            sonuc = "\n\n".join([s.get_text() for s in snippets[:3]])
            return sonuc if sonuc else "Bilgi var ama analiz edilemedi reisim."
        return "Google kapıyı kapattı, sızamadım."
    except Exception as e:
        return f"Bağlantı koptu: {e}"

# --- TELEGRAM BOT KOMUTLARI ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Reis-OS v3 Aktif! Emret reisim, neyi avlayalım?")

async def cevapla(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    await update.message.reply_text("🔍 İnternete sızılıyor, bilgi avlanıyor...")
    
    # İnternetten bilgi çek
    bilgi = internette_avlan(user_msg)
    
    cevap = f"🛡️ **Reis-OS Bilgi Merkezi** 🛡️\n\n{bilgi}\n\n✅ Sistem 7/24 uyanık."
    await update.message.reply_text(cevap)

# --- ANA ÇALIŞTIRICI ---
if __name__ == '__main__':
    # 7/24 sistemi başlat
    keep_alive()
    print("🟢 Reis-OS 7/24 Web Sunucusu Başlatıldı!")

    # Telegram botu başlat
    # BURAYA KENDİ TOKENİNİ YAZ REİSİM
    TOKEN = " 8793626803:AAGRuqr-43_re2L0XjLdup3jda5I3WjD6ac"
    
    nest_asyncio.apply()
    app_telegram = ApplicationBuilder().token(TOKEN).build()
    
    app_telegram.add_handler(CommandHandler("start", start))
    app_telegram.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), cevapla))
    
    print("🟢 Reis-OS Telegram Botu Aktif!")
    app_telegram.run_polling()


