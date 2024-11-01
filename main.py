from datetime import datetime, timedelta
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "7803633885:AAFcyakTVuwrQRAUMxrmFlBQwl44W7rRFsM"
scheduled_messages = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Отправь мне любое сообщение и я отправлю его тебе через 8 часов")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    message_text = update.message.text
    delivery_time = datetime.now() + timedelta(hours=8)
    scheduled_messages[user_id] = {
        'message': message_text,
        'delivery_time': delivery_time
    }
    await update.message.reply_text("Сообщение получено! Я отправлю его тебе через 8 часов")
    await schedule_reminder(user_id, context)

async def schedule_reminder(user_id: int, context: ContextTypes.DEFAULT_TYPE):
    if user_id in scheduled_messages:
        message_info = scheduled_messages[user_id]
        sleep_duration = (message_info['delivery_time'] - datetime.now()).total_seconds()
        if sleep_duration > 0:
            await asyncio.sleep(sleep_duration)
            await context.bot.send_message(
                chat_id=user_id, 
                text=f"Вот твое сообщение, которое ты отправил 8 часов назад:\n\n{message_info['message']}"
            )
            del scheduled_messages[user_id]

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()

if __name__ == '__main__':
    main()