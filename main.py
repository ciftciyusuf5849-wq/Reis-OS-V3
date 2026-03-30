import os
import http.server
import socketserver
from threading import Thread
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# --- 1. RENDER KAPI AYARI (PORT) ---
def keep_alive():
    class HealthCheckHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Reis-OS Online")
    port = int(os.environ.get("PORT", 10000))
    with socketserver.TCPServer(("0.0.0.0", port), HealthCheckHandler) as httpd:
        httpd.serve_forever()

# --- 2. HIZLI ARAMA MOTORU (DUCKDUCKGO) ---
def hizli_ara(sorgu):
    try:
        # DuckDuckGo üzerinden hızlıca sonuç çekiyoruz
        url = f"https://api.duckduckgo.com/?q={sorgu}&format=json&no_html=1"
        res = requests.get(url).json()
        
        if res.get("AbstractText"):
            return f"📝 **İstihbarat:** {res['AbstractText']}\n\n🔗 **Kaynak:** {res['AbstractURL']}"
        elif res.get("RelatedTopics"):
            ilk_sonuc = res["RelatedTopics"][0]
            return f"📝 **Özet Bilgi:** {ilk_sonuc['Text']}\n\n🔗 **Kaynak:** {ilk_sonuc['FirstURL']}"
        else:
            return "🔴 Reisim bu konuda net bir istihbarat bulamadım, başka bir şekilde soralım."
    except:
        return "🔴 Arama motoruna sızarken bir sorun çıktı reis."

# --- 3. TELEGRAM BOT AYARLARI ---
TOKEN = "8793626803:AAGRuqr-43_re2L0XjLdup3jda5I3WjD6ac" # Kendi tokenini buraya mühürle

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🛡️ Reis-OS v4 Yayında! Her şeyi sorabilirsin reisim.")

async def cevapla(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sorgu = update.message.text
    bekle = await update.message.reply_text("🔍 Bilgi merkezine sızıyorum...")
    
    cevap = hizli_ara(sorgu)
    await context.bot.edit_message_text(chat_id=update.effective_chat.id, message_id=bekle.message_id, text=cevap)

if __name__ == '__main__':
    Thread(target=keep_alive, daemon=True).start()
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), cevapla))
    app.run_polling(drop_pending_updates=True)






    
    



