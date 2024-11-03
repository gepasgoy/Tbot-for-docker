import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command
from dotenv import find_dotenv,load_dotenv

load_dotenv(find_dotenv())
token = os.getenv("TOKEN")

bot = Bot(f"{token}")
dp = Dispatcher()


@dp.message(Command("start"))
async def hello(message: Message):
     await message.answer(f"Здравья желаю, {message.from_user.first_name}")

@dp.message(Command("ping"))
async def ping(message: Message):
     await message.answer(f"Pong!")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())