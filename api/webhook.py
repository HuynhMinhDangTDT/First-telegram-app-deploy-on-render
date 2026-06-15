import os
from flask import Flask, request, jsonify
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler

app = Flask(__name__)
TOKEN = os.getenv("TELEGRAM_TOKEN", "8601184029:AAFVeAxydN6Xi06g4SMsDN32vuywhC8iyuc")

# Khởi tạo Telegram App (Cơ chế Webhook)
telegram_app = Application.builder().token(TOKEN).updater(None).build()

# 1. Xử lý lệnh /game hoặc /start
async def start_game(update: Update, context) -> None:
    # Gửi một tin nhắn giới thiệu Game. 
    # Lưu ý: "egg_catcher" là "short_name" của game mà bạn sẽ tạo trên BotFather ở Bước 5
    await update.message.reply_game(game_short_name="egg_catcher")

# 2. Xử lý khi người dùng bấm vào nút "Chơi game"
async def callback_game(update: Update, context) -> None:
    query = update.callback_query
    
    # Kiểm tra xem có đúng là người dùng muốn chơi game "egg_catcher" không
    if query.game_short_name == "egg_catcher":
        # Lấy domain của Vercel từ chính request hoặc cấu hình cố định
        # Để an toàn, bạn có thể thay trực tiếp link Vercel của bạn vào đây:
        vercel_domain = f"https://{request.host}"
        game_url = f"{vercel_domain}/game.html"
        
        # Gửi đường link game để Telegram mở cửa sổ pop-up chơi game
        await query.answer(url=game_url)

# Đăng ký các bộ xử lý
telegram_app.add_handler(CommandHandler("start", start_game))
telegram_app.add_handler(CommandHandler("game", start_game))
telegram_app.add_handler(CallbackQueryHandler(callback_game))

@app.route('/api/webhook', methods=['POST'])
async def webhook():
    if request.method == "POST":
        try:
            data = request.get_json()
            update = Update.de_json(data, telegram_app.bot)
            async with telegram_app:
                await telegram_app.process_update(update)
            return jsonify({"status": "success"}), 200
        except Exception as e:
            print(f"Lỗi: {e}")
            return jsonify({"status": "error", "message": str(e)}), 500
    return "OK", 200

@app.route('/')
def index():
    return "Bot Game đang hoạt động!"