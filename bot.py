import os
import asyncio
import httpx
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from aiogram.types import Message
from aiogram.filters import Command
from models import BotSession
from database import SessionLocal
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery

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

async def get_access_token(telegram_id:int):
    if telegram_id in user_tokens:
        return user_tokens[telegram_id]
    db=SessionLocal()
    try:
        session = db.query(BotSession).filter(BotSession.telegram_id == telegram_id).first()
        if session is None:
            return None
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{API_URL}/refresh",json = {"refresh_token": session.refresh_token})
        if response.status_code != 200:
            return None
        access_token = response.json()["access_token"]
        user_tokens[telegram_id] = access_token
        return access_token
    finally:
        db.close()


class CategoryCallback(CallbackData,prefix = "cat"):
    category_id: int

class NoteAction(CallbackData,prefix = "note"):
    action: str #add , delete , back
    category_id: int

@dp.message(Command("start"))
async def start(message: Message):
    token = await get_access_token(message.from_user.id)

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
    if not token:
        return

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{API_URL}/categories",
            headers= {"Authorization":f"Bearer {token}"}
        )
        if response.status_code != 200:
            return

        categories = response.json()
        if not categories:
            await message.answer("У тебя пока нет категорий. Создай через /new_category <название>")
            return

        buttons = [
            [InlineKeyboardButton(
                text = f"{cat['name']}",
                callback_data = CategoryCallback(category_id = cat['id']).pack()
        )]
        for cat in categories
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard = buttons)
    await message.answer("Твои категории:", reply_markup = keyboard)



@dp.callback_query(CategoryCallback.filter())
async def show_category_notes(callback: CallbackQuery,callback_data:CategoryCallback):
    token = await get_access_token(callback.from_user.id)
    headers = {"Authorization":f"Bearer {token}"}
    if not token:
        return
    async with httpx.AsyncClient() as client:
        category_response = await client.get(
            f"{API_URL}/categories/{callback_data.category_id}",
            headers=headers
        )
        notes_response = await client.get(
            f"{API_URL}/categories/{callback_data.category_id}/notes",
            headers=headers
        )
    categories = category_response.json()
    notes = notes_response.json()
    if not notes:
        text = f"{categories['name']}\n\nНет заметок"
    else:
        text = f"{categories['name']}\n\n"
        for note in notes:
            text += f"{note['title']}\n\n"
    keyboard = InlineKeyboardMarkup(inline_keyboard = [
        [
        InlineKeyboardButton(text = "Добавить",callback_data = NoteAction(action = "add",category_id = callback_data.category_id).pack()),
        InlineKeyboardButton(text = "Удалить",callback_data = NoteAction(action="delete",category_Id = callback_data.category_id).pack()),
        ],
        [
            InlineKeyboardButton(text = "Назад",callback_data = NoteAction(action = "back",category_id = callback_data.category_id).pack()),
        ]
    ])
    await callback.message.edit_text(text,reply_markup = keyboard)
    await callback.answer()

@dp.message(Command("register"))
async def register(message: Message):
    parts = message.text.strip().split()
    if len(parts) != 3:
        await message.answer("Используй : /register <username> <password>")
        return
    _,username,password = parts
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{API_URL}/register",json = {"username":username,"password":password})
    if response.status_code == 200:
        await message.answer(f"Пользователь {username} зарегистрирован. Теперь войди через /login")
    elif response.status_code == 400:
        await message.answer("Пользователь с таким именем уже существует")
    else:
        await message.answer("Ошибка регистрации")



@dp.message(Command("login"))
async def login(message: Message):
    parts = message.text.strip().split()
    if len(parts) != 3:
        await message.answer("Используй : /login <username> <password>")
        return
    _,username,password = parts
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{API_URL}/token",data = {"username":username,"password":password})
    if response.status_code != 200:
        await message.answer("Неверный логин или пароль")
        return
    access_token = response.json()["access_token"]
    refresh_token = response.json()["refresh_token"]
    user_tokens[message.from_user.id] = access_token
    db=SessionLocal()
    try:
        session = db.query(BotSession).filter(BotSession.telegram_id == message.from_user.id).first()
        if session:
            session.refresh_token = refresh_token
        else:
            db.add(BotSession(telegram_id = message.from_user.id,refresh_token = refresh_token))
        db.commit()
    finally:
        db.close()
    await message.answer(f"Добро пожаловать {username}")


@dp.message(Command("categories"))
async def categories(message: Message):
    token = await get_access_token(message.from_user.id)
    if token is None:
        await message.answer("Сначала войдите в аккаунт")
        return
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_URL}/categories",headers= {"Authorization":f"Bearer {token}"})
    if response.status_code != 200:
        await message.answer("Ошибка получения категорий")
        return
    data = response.json()
    if data is None:
        await message.answer("У вас пока нет категорий, Создай через /new_category <название>")
        return
    text = "Твои категории\n\n"
    for category in data:
        text +=f"{category['id']} {category['name']}\n"
    await message.answer(text)



@dp.message(Command("new_category"))
async def new_category(message: Message):
    parts = message.text.strip().split(maxsplit = 1)
    if len(parts) != 2:
        await message.answer("Используй: /new_category <название>")
        return
    name = parts[1]
    token = await get_access_token(message.from_user.id)
    if token is None:
        await message.answer("Сначала войдите в аккаунт")
        return
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{API_URL}/categories",json = {"name":name},headers= {"Authorization":f"Bearer {token}"})
    if response.status_code == 200:
        await message.answer("Категория успешно создана")
    else:
        await message.answer("Ошибка при создании категории")



@dp.message(Command("notes"))
async def notes(message: Message):
    parts = message.text.strip().split()
    if len(parts) != 2 or not parts[1].isdigit():
        await message.answer("Используй: /notes <category_id>")
        return
    category_id = int(parts[1])
    token = await get_access_token(message.from_user.id)
    if token is None:
        await message.answer("Сначала войдите в аккаунт")
        return
    async with httpx.AsyncClient() as client:
        category_response = await client.get(
            f"{API_URL}/categories/{category_id}",
            headers = {"Authorization":f"Bearer {token}"}
        )
        if category_response.status_code == 404:
            await message.answer("Ошибка, категория не найдена")
            return

        response = await client.get(
            f"{API_URL}/categories/{category_id}/notes",
            headers= {"Authorization":f"Bearer {token}"}
        )
    category = category_response.json()
    data = response.json()
    if not data:
        await message.answer("В этой категории пока нет заметок. Добавь через /add")
        return
    text = f"|{category['name']}|\n"
    for notes in data:
        text += f"{notes['id']} {notes['title']} \n"
    await message.answer(text)


@dp.message(Command("add"))
async def add_note(message: Message):
    parts = message.text.strip().split(maxsplit = 2)
    if len(parts) != 3 or not parts[1].isdigit():
        await message.answer("Используй: /add <category_id> <заметка>")
        return
    category_id = int(parts[1])
    title = parts[2]
    token = await get_access_token(message.from_user.id)
    if not token:
        await message.answer("Сначала войди через /login")
        return
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{API_URL}/notes",
            json = {"title": title, "category_id": category_id},
            headers= {"Authorization":f"Bearer {token}"}
        )
    if response.status_code == 200:
        await message.answer(f"Заметка {title} успешно создана")
    else:
        await message.answer(f"Ошибка:{response.status_code}")


@dp.message(Command("delete"))
async def delete_note(message: Message):
    parts = message.text.strip().split()
    if len(parts) != 2 or not parts[1].isdigit():
        await message.answer("Используй: /notes <category_id>")
        return
    _,note_id = parts
    token = await get_access_token(message.from_user.id)
    if not token:
        await message.answer("Сначала войдите в аккаунт")
        return
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{API_URL}/notes/{note_id}",headers= {"Authorization":f"Bearer {token}"})
    if response.status_code == 200:
        await message.answer("Заметка удалена")
    elif response.status_code == 404:
        await message.answer("Заметка не найдена")
    else:
        await message.answer("Ошибка удаления")


@dp.message()
async def fallback(message: Message):
    await message.answer("Используй /start чтобы увидеть список команд")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())