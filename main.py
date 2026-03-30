import os
import http.server
import socketserver
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# --- RENDER'I SUSTURACAK BASİT SUNUCU ---
def keep_alive():
    class HealthCheckHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Reis-OS Aktif!")

    port = int(os.environ.get("PORT", 10000))
    with socketserver.TCPServer(("0.0.0.0", port), HealthCheckHandler) as httpd:
        print(f"🟢 Render Kapısı Açıldı: {port}")
        httpd.serve_forever()

# --- TELEGRAM BOT KODLARI ---
TOKEN = "8793626803:AAGRuqr-43_re2L0XjLdup3jda5I3WjD6ac" # Tokenini buraya mühürle reis

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🛡️ Reis-OS v3 Çelik Gibi Aktif! Emret reisim.")

async def cevapla(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    await update.message.reply_text(f"🔍 Mesajın merkezde işleniyor reis: {user_msg}")

if __name__ == '__main__':
    # Önce Render'ı kandıracak sunucuyu başlatıyoruz
    Thread(target=keep_alive, daemon=True).start()
    
    # Sonra botu ateşliyoruz
    print("🟢 Bot sahalara iniyor...")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), cevapla))
    
    app.run_polling(drop_pending_updates=True)



    
    



