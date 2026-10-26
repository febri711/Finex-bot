import os
import threading
import requests
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.environ.get("BOT_TOKEN", "ISI_TOKEN_BOT_LU_DISINI")
app = Flask(__name__)

@app.route('/')
def home():
    return "Finex Bot Running! 🚀"

@app.route('/health')
def health():
    return "OK", 200

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txt = "🔥 *FINEX BOT SIAP BOS!* 🔥\n\nGue asisten trading crypto lu.\n\nPerintah:\n/start - Menu\n/harga btc - Cek harga\n/analisa btc - Analisa\n\nTanya aja: btc mau naik gak?"
    await update.message.reply_text(txt, parse_mode="Markdown")

async def harga(update: Update, context: ContextTypes.DEFAULT_TYPE):
    coin = "bitcoin"
    if context.args:
        a = context.args[0].lower()
        if a == "btc": coin = "bitcoin"
        elif a == "eth": coin = "ethereum"
        elif a == "sol": coin = "solana"
        else: coin = a
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd,idr&include_24hr_change=true"
        r = requests.get(url, timeout=10).json()
        d = r[coin]
        usd = d['usd']
        idr = d['idr']
        ch = d.get('usd_24h_change',0)
        emo = "🟢" if ch>=0 else "🔴"
        await update.message.reply_text(f"{emo} *{coin.upper()}*\n💵 ${usd:,.2f}\n💰 Rp {idr:,.0f}\n📈 24h: {ch:.2f}%", parse_mode="Markdown")
    except:
        await update.message.reply_text("Coin gak ketemu bos, coba /harga btc")

async def analisa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    c = context.args[0].upper() if context.args else "BTC"
    await update.message.reply_text(f"📊 *ANALISA {c}*\nTrend: Bullish tipis 🟢\nSupport -2%\nResistance +3.5%\n\nJangan FOMO, masuk nyicil 30% aja. DYOR!", parse_mode="Markdown")

async def chat_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.message.text.lower()
    if "btc" in q: await update.message.reply_text("BTC konsolidasi bos, jebol 110k bisa terbang. Sabar!")
    elif "beli" in q: await update.message.reply_text("Aturan Finex: Beli nyicil 3x, jangan all-in bos!")
    else: await update.message.reply_text("Tanya soal crypto bos! /harga btc")

def run_bot():
    app_ = ApplicationBuilder().token(BOT_TOKEN).build()
    app_.add_handler(CommandHandler("start", start))
    app_.add_handler(CommandHandler("harga", harga))
    app_.add_handler(CommandHandler("price", harga))
    app_.add_handler(CommandHandler("analisa", analisa))
    app_.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_ai))
    app_.run_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
