import os
import random
import requests
import asyncio
import nest_asyncio
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# --- HAYALET MODU İNTERNET AVCI FONKSİYONU ---
def internette_avlan(sorgu):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}
    url = f"https://www.google.com/search?q={sorgu}&hl=tr"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        snippets = soup.find_all("div", class_="VwiC3b") 
        sonuc = "\n\n".join([s.get_text() for s in snippets[:3]])
        return sonuc if sonuc else "Bilgi avlandı ama analiz edilemedi reisim."
    except:
        return "Bağlantı koptu, tekrar dene reisim."

# --- BOT KOMUTLARI ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Reis-OS v3 Nöbette! Emret reisim.")

async def cevapla(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    await update.message.reply_text("🔍 İnternetin derinliklerine sızılıyor...")
    bilgi = internette_avlan(user_msg)
    await update.message.reply_text(f"🛡️ **Bilgi Merkezi** 🛡️\n\n{bilgi}")

# --- ANA ÇALIŞTIRICI ---
if __name__ == '__main__':
    # TOKENİ BURAYA YAPIŞTIR REİSİM
    TOKEN = "8793626803:AAGRuqr-43_re2L0XjLdup3jda5I3WjD6ac"
    
    nest_asyncio.apply()
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app_telegram = app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), cevapla))
    
    print("🟢 Bot Ayağa Kalktı!")
    app.run_polling()

    
    



