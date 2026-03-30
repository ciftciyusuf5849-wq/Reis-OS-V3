import os
import http.server
import socketserver
from threading import Thread
from googlesearch import search
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# --- 1. RENDER'I SUSTURAN GARANTİ KAPI ---
def keep_alive():
    class HealthCheckHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Sistem Celik Gibi!")
    port = int(os.environ.get("PORT", 10000))
    with socketserver.TCPServer(("0.0.0.0", port), HealthCheckHandler) as httpd:
        httpd.serve_forever()

# --- 2. TELEGRAM BOT AYARLARI ---
TOKEN = "8793626803:AAGRuqr-43_re2L0XjLdup3jda5I3WjD6ac" # Reis, tokenini buraya dikkatlice yaz

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🛡️ Reis-OS v3 Devrede! Yolumuz uzun, yükümüz ağır. Emret reisim.")

async def ara_ve_cevapla(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    # "num" veya "stop" parametresi olmadan, en sade haliyle arıyoruz
    try:
        bekleme = await update.message.reply_text("🔍 İstihbarat toplanıyor...")
        
        sonuclar = []
        # En basit ve hatasız döngü
        search_results = search(query, lang='tr')
        
        for i, url in enumerate(search_results):
            if i < 3: # Sadece ilk 3 linki alıyoruz
                sonuclar.append(f"🔹 Kaynak {i+1}: {url}")
            else:
                break
        
        if sonuclar:
            cevap = "🌐 Bulduğum bilgiler şunlar reisim:\n\n" + "\n".join(sonuclar)
        else:
            cevap = "🔴 Reisim internette tık yok, konu çok derin herhalde."
            
        await context.bot.edit_message_text(chat_id=update.effective_chat.id, message_id=bekleme.message_id, text=cevap)
        
    except Exception as e:
        # Hata olursa bota değil, sadece panele yazdırıyoruz ki seni darlamasın
        print(f"Hata: {e}")
        await update.message.reply_text("🔴 Operasyonda ufak bir pürüz çıktı ama bot hala ayakta.")

if __name__ == '__main__':
    # Önce Render'ı sustur, sonra botu ateşle
    Thread(target=keep_alive, daemon=True).start()
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), ara_ve_cevapla))
    
    print("🟢 Bot sahalarda!")
    app.run_polling(drop_pending_updates=True)





    
    



