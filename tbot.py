import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command
from dotenv import find_dotenv,load_dotenv
import socket
import threading

load_dotenv(find_dotenv())
token = os.getenv("TOKEN")

bot = Bot(f"{token}")
dp = Dispatcher()

def start_server_in_thread():
  server_thread = threading.Thread(target=start_server)
  server_thread.daemon = True # Устанавливаем поток как "демон"
  server_thread.start()
  print("Сервер работает в фоновом потоке.")


@dp.message(Command("start"))
async def hello(message: Message):
     await message.answer(f"Здравья желаю, {message.from_user.first_name}")

@dp.message(Command("ping"))
async def ping(message: Message):
    await message.answer(f"Pong!")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

def start_server():
  # Создаем сокет
  server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  # Указываем IP-адрес и порт для прослушивания (в данном случае 8080)
  host = '0.0.0.0'
  port = 8080

  # Связываем сокет с адресом и портом
  server_socket.bind((host, port))

  # Запускаем прослушивание
  server_socket.listen(5)
  print(f"Сервер запущен и прослушивает порт {port}...")

  while True:
    # Ожидаем подключения
    client_socket, address = server_socket.accept()
    print(f"Подключение от {address}")

    # Получаем данные от клиента
    data = client_socket.recv(1024).decode()
    print(f"Данные от клиента: {data}")

    # Отправляем ответ клиенту
    response = "HTTP/1.1 200 OK\n\nПривет, клиент!"
    client_socket.send(response.encode())

    # Закрываем соединение с клиентом
    client_socket.close()


if __name__ == "__main__":
    start_server_in_thread()
    asyncio.run(main())