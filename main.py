from aiogram import Bot, Dispatcher, F
from aiogram.types import BotCommand
from asyncio import run
from function import start, report, user_finder, add_admin, rm_admin
import sqlite3

db = sqlite3.connect('my_database.db')
cursor = db.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS ids (user_id int, unique_id int)')
cursor.execute('CREATE TABLE IF NOT EXISTS admins (admin_id int)')
db.commit()


async def main():
    dp = Dispatcher()
    bot = Bot(token='7683748418:AAGjY8dBLD216KjpbGGeaI1E9U9xM6es43o')
    dp.message.register(start, F.text == '/start')
    dp.message.register(user_finder, F.text.startswith('/finder'))
    dp.message.register(add_admin, F.text.startswith('/add_admin'))
    dp.message.register(rm_admin, F.text.startswith('/rm_admin'))
    dp.message.register(report)
    await bot.set_my_commands([
        BotCommand(command='start', description='Botni ishga tushirish'),
    ])        
    await dp.start_polling(bot, polling_timeout=1)

if __name__ == '__main__':
    run(main())