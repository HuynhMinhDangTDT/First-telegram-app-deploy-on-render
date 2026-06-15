import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Lấy Token từ biến môi trường (an toàn hơn khi deploy)
TOKEN = os.getenv("TELEGRAM_TOKEN", "8601184029:AAFVeAxydN6Xi06g4SMsDN32vuywhC8iyuc")

# Hàm xử lý khi người dùng gõ /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Tạo các nút nhấn
    keyboard = [
        [
            InlineKeyboardButton("Nút số 1 🚀", callback_data="btn_1"),
            InlineKeyboardButton("Nút số 2 🎉", callback_data="btn_2"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Gửi tin nhắn kèm nút
    await update.message.reply_text("Chào bạn! Hãy thử nhấn vào một trong các nút bên dưới:", reply_markup=reply_markup)

# Hàm xử lý khi người dùng nhấn vào nút
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    # Bắt buộc phải phản hồi lại query để nút bấm dừng hiệu ứng "đang tải"
    await query.answer()
    
    # Kiểm tra xem người dùng bấm nút nào dựa vào callback_data
    if query.data == "btn_1":
        await query.edit_message_text(text="Bạn vừa nhấn **Nút số 1**! Tuyệt vời.")
    elif query.data == "btn_2":
        await query.edit_message_text(text="Bạn vừa nhấn **Nút số 2**! Quá đỉnh.")

def main():
    # Khởi tạo ứng dụng bot
    application = Application.builder().token(TOKEN).build()

    # Đăng ký các bộ xử lý lệnh (handlers)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_click))

    # Bắt đầu chạy bot bằng cơ chế Polling (liên tục kiểm tra tin nhắn mới)
    print("Bot đang chạy...")
    application.run_polling()

if __name__ == "__main__":
    main()