import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from environs import Env

env = Env()
_ = env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN yo‘q, .env faylga yoz!")

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: Message):
    user = message.from_user  
    
    info = (
        f"👤 <b>Foydalanuvchi maʼlumotlari</b>\n\n"
        f"🆔 <b>ID:</b> <code>{user.id}</code>\n"
        f"👨‍💻 <b>Username:</b> @{user.username if user.username else '—'}\n"
        f"📛 <b>Full name:</b> {user.full_name}\n"
        f"📄 <b>First name:</b> {user.first_name}\n"
        f"📄 <b>Last name:</b> {user.last_name if user.last_name else '—'}\n"
        f"🌐 <b>Language:</b> {user.language_code or '—'}"
    )

    await message.answer(info, parse_mode="HTML")

async def main():
    print("Bot ishga tushmoqda...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
