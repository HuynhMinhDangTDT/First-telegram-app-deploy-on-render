import os
import threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- PHẦN 1: TẠO FLASK APP GIẢ ĐỂ HUGGING FACE KHÔNG BÁO LỖI ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot Telegram đang chạy ngon lành!"

def run_flask():
    # Chạy Flask trên cổng 7860 (cổng mặc định của Hugging Face)
    app.run(host="0.0.0.0", port=7860)
# -------------------------------------------------------------

# --- PHẦN 2: CODE BOT TELEGRAM CỦA BẠN ---
TOKEN = os.getenv("TELEGRAM_TOKEN", "THAY_TOKEN_CỦA_BẠN_VÀO_ĐÂY")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [
            InlineKeyboardButton("Nút số 1 🚀", callback_data="btn_1"),
            InlineKeyboardButton("Nút số 2 🎉", callback_data="btn_2"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Chào bạn! Hãy thử nhấn vào một trong các nút bên dưới:", reply_markup=reply_markup)

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    if query.data == "btn_1":
        await query.edit_message_text(text="Bạn vừa nhấn **Nút số 1**! Tuyệt vời.")
    elif query.data == "btn_2":
        await query.edit_message_text(text="Bạn vừa nhấn **Nút số 2**! Quá đỉnh.")

def run_bot():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_click))
    print("Bot đang chạy...")
    application.run_polling()
# ----------------------------------------

if __name__ == "__main__":
    # Dùng Threading để chạy song song cả Flask (đối phó hệ thống) và Bot Telegram cùng một lúc
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
    
    # Chạy Bot Telegram
    run_bot()