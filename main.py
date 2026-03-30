import os
import http.server
import socketserver
from threading import Thread
from googlesearch import search
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# --- RENDER'I AYAKTA TUTAN KAPI ---
def keep_alive():
    class HealthCheckHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Reis-OS v3 Online")
    port = int(os.environ.get("PORT", 10000))
    with socketserver.TCPServer(("0.0.0.0", port), HealthCheckHandler) as httpd:
        httpd.serve_forever()

# --- BOTUN BEYNİ VE AYARLARI ---
TOKEN = "8793626803:AAGRuqr-43_re2L0XjLdup3jda5I3WjD6ac" # Kendi tokenini mühürle reis

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🛡️ Reis-OS v3 İnternet Avcısı Devrede! Ne arıyoruz reisim?")

async def ara_ve_cevapla(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    bekleme_mesaji = await update.message.reply_text("🔍 İnternetin derinliklerine sızıyorum, bekle reisim...")
    
    try:
        # İnternette ilk 3 sonucu avlıyoruz
        sonuclar = []
        for j in search(query, num=3, stop=3, lang='tr'):
            sonuclar.append(j)
        
        if sonuclar:
            cevap = "🌐 Bulduğum istihbarat şunlar reisim:\n\n" + "\n".join(sonuclar)
        else:
            cevap = "🔴 Reisim internetin dibine kadar indim ama somut bir şey bulamadım."
            
    except Exception as e:
        cevap = f"🔴 Operasyon sırasında bir aksilik çıktı reis: {e}"
    
    await context.bot.edit_message_text(chat_id=update.effective_chat.id, message_id=bekleme_mesaji.message_id, text=cevap)

if __name__ == '__main__':
    Thread(target=keep_alive, daemon=True).start()
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), ara_ve_cevapla))
    
    print("🟢 Reis-OS v3 İnternet Avcısı aktif!")
    app.run_polling(drop_pending_updates=True)




    
    



