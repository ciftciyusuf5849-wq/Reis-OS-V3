import os, http.server, socketserver
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# --- AYARLAR ---
TOKEN = "BURAYA_BOT_TOKENINI_YAZ" # Kendi tokenini buraya mühürle reis

def keep_alive():
    class H(http.server.SimpleHTTPRequestHandler):
        def do_GET(self): 
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Reis-AI Celik Gibi!")
    port = int(os.environ.get("PORT", 10000))
    with socketserver.TCPServer(("0.0.0.0", port), H) as httpd:
        httpd.serve_forever()

async def start(u: Update, c: ContextTypes.DEFAULT_TYPE):
    await u.message.reply_text("🛡️ Reis-AI Yayında! Kredi kartı yok, engel yok, sadece akıl var. Emret reisim.")

async def sohbet(u: Update, c: ContextTypes.DEFAULT_TYPE):
    mesaj = u.message.text.lower()
    
    # Botun kendi zekası (Hızlı Cevaplar)
    if "messi" in mesaj:
        cevap = "⚽ Lionel Messi mi? O bir dünya markası reisim. 8 Ballon d'Or sahibi, tarihin en büyüğü diyebiliriz. Senin için başka neyini araştırayım?"
    elif "erdemli" in mesaj:
        cevap = "🍋 Erdemli mi? Memleketin göz bebeği, narenciyenin başkenti. Havası sert, insanı merttir reisim."
    elif "python" in mesaj:
        cevap = "🐍 Python tam bir ağır abi dilidir reis. Okuması kolay, gücü büyüktür. Senin mobil kodlama projesinde sırtın yere gelmez."
    elif "selam" in mesaj or "merhaba" in mesaj:
        cevap = "Aleykümselam reisim, hoş geldin. Yolumuz uzun, yükümüz ağır. Emrindeyim."
    else:
        cevap = "🔍 Reisim, bu konuyu senin için derinlemesine analiz ediyorum. Şimdilik hafızamdaki bilgiler bunlar, ama her geçen gün kendimi geliştiriyorum!"

    await u.message.reply_text(cevap)

if __name__ == '__main__':
    Thread(target=keep_alive, daemon=True).start()
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), sohbet))
    print("🟢 Reis-AI Sahada!")
    app.run_polling(drop_pending_updates=True)







    
    



