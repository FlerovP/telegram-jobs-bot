# Telegram Jobs Bot

Бот для сбора вакансий из Telegram-групп и каналов. Бот автоматически отслеживает новые сообщения, извлекает информацию о вакансиях и сохраняет их в базу данных.

## Развертывание на Render.com

1. Форкните этот репозиторий
2. Зарегистрируйтесь на [Render.com](https://render.com)
3. Создайте новый Web Service:
   - Подключите ваш GitHub репозиторий
   - Выберите ветку `main`
   - Выберите тип "Worker"
   - Укажите имя сервиса
   - Environment: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python bot.py`
4. Добавьте переменную окружения:
   - `TELEGRAM_BOT_TOKEN`: ваш токен бота от @BotFather

## Локальная разработка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/YOUR_USERNAME/telegram-jobs-bot.git
cd telegram-jobs-bot
```

2. Создайте виртуальное окружение и активируйте его:
```bash
python3 -m venv venv
source venv/bin/activate  # для Linux/Mac
# или
venv\Scripts\activate  # для Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Создайте файл .env и добавьте токен бота:
```
TELEGRAM_BOT_TOKEN=your_bot_token_here
```

5. Запустите бота:
```bash
python bot.py
```

## Команды бота

- `/start` - Начать работу с ботом
- `/help` - Показать справку
- `/stats` - Показать статистику собранных вакансий

## Структура проекта

- `bot.py` - Основной файл бота
- `database.py` - Модуль для работы с базой данных
- `parser.py` - Модуль для парсинга сообщений
- `requirements.txt` - Зависимости проекта
- `.env` - Конфигурационный файл
- `render.yaml` - Конфигурация для развертывания на Render.com

# Job Search Telegram Bot

## Deployment on PythonAnywhere

1. Create a free account on [PythonAnywhere](https://www.pythonanywhere.com)

2. Open a Bash console on PythonAnywhere and run:
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Create a new file `.env` in the project directory with your bot token:
```
TELEGRAM_BOT_TOKEN=your_bot_token_here
```

4. Go to the "Web" tab on PythonAnywhere
   - Add a new web app
   - Choose "Manual Configuration"
   - Choose Python 3.9
   - Set the working directory to your project directory
   - Set the WSGI file path to point to your bot.py

5. Set up an "Always-on task":
   - Go to "Tasks" tab
   - Add a new task
   - Command to run: `python3 /home/YOUR_USERNAME/YOUR_REPO/bot.py`
   - Set it to run daily

## Local Development

1. Clone the repository
2. Create a virtual environment: `python3 -m venv venv`
3. Activate it: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Create `.env` file with your bot token
6. Run the bot: `python bot.py`
