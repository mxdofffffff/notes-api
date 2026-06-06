import os
import asyncio
import httpx
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from aiogram.types import Message
from aiogram.filters import Command
from models import BotSession
from database import SessionLocal

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
API_URL = os.getenv("API_URL","http://localhost:8000")
bot = Bot(TOKEN)
dp = Dispatcher()

user_tokens = {}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "Привет!\n"
        "Доступные команды:\n"
        "/register <username> <password> — регистрация\n"
        "/login <username> <password> — вход\n"
        "/categories — список категорий\n"
        "/new_category <название> — создать категорию\n"
        "/notes <category_id> — заметки в категории\n"
        "/add <category_id> <заметка> — добавить заметку\n"
        "/delete <note_id> — удалить заметку\n"
    )

@dp.message()
async def fallback(message: Message):
    await message.answer("Используй /start чтобы увидеть список команд")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())