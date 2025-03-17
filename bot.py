import logging
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from database import init_db, create_job, job_exists, get_all_jobs
from parser import parse_job_message

# Загружаем переменные окружения
load_dotenv()

# Настраиваем логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Инициализируем базу данных
init_db()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    await update.message.reply_text(
        'Привет! Я бот для сбора вакансий. Я буду автоматически сохранять вакансии из сообщений в этой группе.'
    )

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    await update.message.reply_text(
        'Я автоматически собираю вакансии из сообщений в группе.\n'
        'Доступные команды:\n'
        '/start - Начать работу с ботом\n'
        '/help - Показать это сообщение\n'
        '/stats - Показать статистику собранных вакансий'
    )

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /stats"""
    jobs = get_all_jobs()
    await update.message.reply_text(
        f'Всего собрано вакансий: {len(jobs)}'
    )

async def process_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик новых сообщений"""
    if not update.message or not update.message.text:
        return

    # Парсим информацию о вакансии из сообщения
    job_data = parse_job_message(update.message.text)
    if not job_data:
        return

    # Проверяем, существует ли уже такая вакансия
    if job_exists(update.message.message_id):
        logger.info(f"Вакансия уже существует: {update.message.message_id}")
        return

    # Создаем запись в базе данных
    try:
        create_job(
            title=job_data.get('title'),
            company=job_data.get('company'),
            salary=job_data.get('salary'),
            requirements=job_data.get('requirements'),
            link=job_data.get('link'),
            source=job_data.get('source'),
            message_id=update.message.message_id
        )
        logger.info(f"New job saved: {job_data.get('title')}")
    except Exception as e:
        logger.error(f"Error saving job: {e}")

def main():
    """Основная функция запуска бота"""
    # Получаем токен бота из переменной окружения
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        logger.error("No token provided!")
        return

    # Создаем приложение бота
    application = Application.builder().token(token).build()

    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("stats", stats))

    # Добавляем обработчик сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_message))

    # Запускаем бота
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main() 