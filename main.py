import os
import requests
import time
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# --- BOT AYARLARI ---
# BURAYA KENDİ TOKENİNİ YAZ REİSİM
TOKEN = "8793626803:AAGRuqr-43_re2L0XjLdup3jda5I3WjD6ac"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Reis-OS v3 Sahada! Her şey yolunda reisim.")

async def cevapla(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    # Basit bir cevap mekanizması (İnternet aramasını sonra ekleriz, önce botu bağlayalım)
    await update.message.reply_text(f"Emredersin reisim, mesajını aldım: {user_msg}")

if __name__ == '__main__':
    print("🟢 Bot uyandırılıyor...")
    try:
        app = ApplicationBuilder().token(TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), cevapla))
        
        print("🟢 Telegram bağlantısı kuruldu. Bot aktif!")
        app.run_polling(drop_pending_updates=True)
    except Exception as e:
        print(f"🔴 Hata çıktı: {e}")


    
    



