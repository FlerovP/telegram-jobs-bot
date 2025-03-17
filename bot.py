import logging
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from database import init_db, create_job, job_exists, get_active_jobs
from parser import JobParser

# Загружаем переменные окружения
load_dotenv()

# Настраиваем логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=os.getenv('LOG_LEVEL', 'INFO')
)
logger = logging.getLogger(__name__)

# Инициализируем парсер вакансий
job_parser = JobParser()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    await update.message.reply_text(
        'Привет! Я бот для сбора вакансий. '
        'Добавьте меня в группу, и я буду отслеживать все новые вакансии.'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    help_text = """
Я помогаю собирать вакансии из групп Telegram.

Основные команды:
/start - Начать работу с ботом
/help - Показать это сообщение
/stats - Показать статистику собранных вакансий

Для работы просто добавьте меня в группу, где публикуются вакансии.
    """
    await update.message.reply_text(help_text)

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /stats"""
    jobs = get_active_jobs()
    
    if not jobs:
        await update.message.reply_text("Пока не собрано ни одной вакансии.")
        return

    response = f"📊 Всего собрано вакансий: {len(jobs)}\n\n"
    response += "🔍 Последние 5 вакансий:\n\n"

    for job in jobs[-5:]:
        response += f"📌 {job.title}\n"
        if job.company:
            response += f"🏢 Компания: {job.company}\n"
        if job.salary:
            response += f"💰 Зарплата: {job.salary}\n"
        if job.location:
            response += f"📍 Локация: {job.location}\n"
        if job.source_link:
            response += f"🔗 Ссылка: {job.source_link}\n"
        response += "\n"

    await update.message.reply_text(response)

async def process_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик новых сообщений"""
    try:
        # Проверяем, что сообщение из группы
        if not update.message.chat.type in ['group', 'supergroup']:
            return

        # Получаем текст сообщения
        text = update.message.text
        if not text:
            return

        # Проверяем, существует ли уже такая вакансия
        if job_exists(update.message.message_id, update.message.chat_id):
            logger.info(f"Вакансия уже существует: {update.message.message_id}")
            return

        # Парсим информацию о вакансии
        job_details = job_parser.extract_job_details(text)

        # Если не удалось определить заголовок, пропускаем сообщение
        if not job_details['title']:
            return

        # Создаем запись в базе данных
        job = create_job(
            title=job_details['title'],
            company=job_details['company'],
            description=job_details['description'],
            salary=job_details['salary'],
            location=job_details['location'],
            requirements=job_details['requirements'],
            contact=job_details['contact'],
            telegram_message_id=update.message.message_id,
            telegram_chat_id=update.message.chat_id,
            source_link=f"https://t.me/{update.message.chat.username}/{update.message.message_id}" if update.message.chat.username else None
        )

        logger.info(f"Создана новая вакансия: {job}")

    except Exception as e:
        logger.error(f"Ошибка при обработке сообщения: {e}", exc_info=True)

def main():
    """Основная функция запуска бота"""
    # Инициализируем базу данных
    init_db()

    # Создаем приложение бота
    application = Application.builder().token(os.getenv('TELEGRAM_BOT_TOKEN')).build()

    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("stats", stats_command))

    # Добавляем обработчик сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_message))

    # Запускаем бота
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main() 