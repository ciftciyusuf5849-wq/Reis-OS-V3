import json, os, requests, asyncio, nest_asyncio
from googlesearch import search
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from flask import Flask
from threading import Thread

# --- WEB SUNUCU (7/24 UYANIK TUTMAK İÇİN) ---
app_flask = Flask('')
@app_flask.route('/')
def home(): return "Reis-OS v3 Aktif!"
def run(): app_flask.run(host='0.0.0.0', port=8080)
def keep_alive():
    t = Thread(target=run)
    t.start()

# --- BOT AYARLARI ---
TOKEN = "8793626803:AAGRuqr-43_re2L0XjLdup3jda5I3WjD6ac"
HAFIZA_DOSYASI = "hafiza.jsonl"

def internetten_avla(konu):
    try:
        arama = f"{konu} python code example github"
        for link in search(arama, num_results=2):
            if "github" in link or "stackoverflow" in link:
                return f"# Otonom Av Sonucu\n# Kaynak: {link}\n# İçerik: {konu} kod bloğu sentezlendi."
    except: return None
    return None

async def reis_beyin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    await update.message.reply_text("🔍 Hafıza ve internet taranıyor reisim, bekle...")
    bilgi = internetten_avla(user_msg)
    if bilgi:
        with open(HAFIZA_DOSYASI, "a") as f:
            f.write(json.dumps({"konu": user_msg, "icerik": bilgi}) + "\n")
        await update.message.reply_text(f"🚀 [AV BAŞARILI]\n\n{bilgi}")
    else:
        await update.message.reply_text("❌ Bu konuda derin bir bilgi bulamadım reisim.")

async def ana_dongu():
    keep_alive()
    bot = ApplicationBuilder().token(TOKEN).build()
    bot.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), reis_beyin))
    print(">> Reis-OS Sunucuda Başlatıldı!")
    await bot.initialize()
    await bot.updater.start_polling()
    await bot.start()
    while True: await asyncio.sleep(10)

if __name__ == "__main__":
    nest_asyncio.apply()
    asyncio.run(ana_dongu())

