import random
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler

TOKEN = "ВАШ_ТОКЕН_БОТА"
CHAT_ID = "ВАШ_CHAT_ID"

# Функція для читання повідомлень
def get_random_message():
    with open("messages.txt", "r", encoding="utf-8") as file:
        messages = file.readlines()
    return random.choice(messages).strip()

# Функція для відправки повідомлення
async def send_random_message(chat_id):
    bot = Bot(token=TOKEN)
    await bot.send_message(chat_id=chat_id, text=get_random_message())

# Команда /start з кнопкою
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Отримати рандомне повідомлення💌", callback_data="random_msg")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("💌Натисніть кнопку для отримання повідомлення:", reply_markup=reply_markup)

# Обробник кнопки
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await send_random_message(query.message.chat_id)

# Планувальник для щоденних повідомлень
async def scheduled_message():
    await send_random_message(CHAT_ID)

if __name__ == "__main__":
    application = Application.builder().token(TOKEN).build()
    
    # Додаємо обробники
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # Налаштування планувальника
    scheduler = AsyncIOScheduler()
    scheduler.add_job(scheduled_message, "cron", hour=10)  # 12:00 Київський час
    scheduler.start()
    
    application.run_polling()
