import os
from flask import Flask, request, jsonify
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Khởi tạo Flask App
app = Flask(__name__)

# Lấy Token an toàn từ biến môi trường (Hệ thống sẽ tự lấy Token mới bạn đã đổi trong Vercel Settings)
TOKEN = os.getenv("TELEGRAM_TOKEN", "8601184029:AAFVeAxydN6Xi06g4SMsDN32vuywhC8iyuc")

# Khởi tạo Telegram Application theo cơ chế Webhook (Bật updater=None)
telegram_app = Application.builder().token(TOKEN).updater(None).build()

# --- 1. XỬ LÝ LỆNH /START HOẶC /GAME ---
async def start_game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Gửi tin nhắn mời chơi game. "egg_catcher" là short_name bạn đã tạo trên @BotFather
    await update.message.reply_game(game_short_name="egg_catcher")

# --- 2. XỬ LÝ KHI NGƯỜI DÙNG BẤM NÚT "PLAY" TRÊN TELEGRAM ---
async def callback_game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    
    if query.game_short_name == "egg_catcher":
        # Tự động nhận diện domain (Dù chạy ở localhost hay trên Vercel thực tế)
        vercel_domain = f"https://{request.host}" if "localhost" not in request.host else f"http://{request.host}"
        game_url = f"{vercel_domain}/game.html"
        
        # Trả về đường dẫn để Telegram mở cửa sổ Pop-up Webview chơi game
        await query.answer(url=game_url)

# Đăng ký các bộ xử lý lệnh và nút bấm vào hệ thống
telegram_app.add_handler(CommandHandler("start", start_game))
telegram_app.add_handler(CommandHandler("game", start_game))
telegram_app.add_handler(CallbackQueryHandler(callback_game))

# --- 3. ĐƯỜNG DẪN (ROUTE) NHẬN DỮ LIỆU WEBHOOK TỪ TELEGRAM ---
@app.route('/api/webhook', methods=['POST'])
async def webhook():
    if request.method == "POST":
        try:
            data = request.get_json()
            update = Update.de_json(data, telegram_app.bot)
            
            # Xử lý sự kiện tin nhắn đồng bộ với Flask bằng "async with"
            async with telegram_app:
                await telegram_app.process_update(update)
                
            return jsonify({"status": "success"}), 200
        except Exception as e:
            print(f"Lỗi xử lý webhook: {e}")
            return jsonify({"status": "error", "message": str(e)}), 500
    return "OK", 200

# Trang chủ hiển thị khi truy cập trực tiếp bằng trình duyệt
@app.route('/')
def index():
    return "Bot Game Telegram đang hoạt động mượt mà trên Vercel!"

# --- 4. KHỐI LỆNH CHẠY DƯỚI MÁY LOCAL (MINICONDA) ---
if __name__ == "__main__":
    print("--- ĐANG CHẠY FLASK TRÊN MÁY LOCAL ---")
    print("Mở trình duyệt truy cập: http://127.0.0.1:8080")
    # debug=True giúp tự động tải lại code khi bạn sửa file
    app.run(host="0.0.0.0", port=7860)