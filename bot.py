from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties

import asyncio
import logging

from utils.parsers import get_programs_info  # Импорт парсера

from ollama import chat
from ollama import ChatResponse

programs_data = []

TOKEN = 'YOUR-TOKEN-HERE'
logging.basicConfig(level=logging.INFO)

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    )
)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: Message):
    text = (
        'Привет! Я помогу тебе с выбором программы для обучения!\n\n'
        'Ты можешь задавать вопросы по следующим программам:\n'
    )
    for program in programs_data:
        text += f"📌 <b>{program['name']}</b>\n"
    await message.answer(text)


@dp.message()
async def handle_user_question(message: Message):
    global programs_data
    user_text = message.text.strip()

    response: ChatResponse = chat(model='llama3.2', messages=[
        {
            'role': 'system',
            'content': f'Используй следующую информацию при ответах: {str(programs_data)}'
        },
        {
            'role': 'user',
            'content': user_text
        },
    ])

    await message.answer(response.message.content)

# Запуск бота
async def main():
    global programs_data
    programs_data = get_programs_info()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
