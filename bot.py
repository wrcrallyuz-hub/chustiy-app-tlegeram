import asyncio
import json
import logging
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    WebAppInfo,
)

# 1. @BotFather dan olingan bot tokenni shu yerga yozing:
BOT_TOKEN = "SIZNING_BOT_TOKENINGIZ"

# 2. Mini App sayti havolasi (GitHub Pages, Vercel yoki lokal ngrok):
WEBAPP_URL = "https://your-domain.com/telegram_miniapp_chustiy.html"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_handler(message: types.Message):
    """Foydalanuvchi /start bosganda Mini App tugmasini yuborish"""
    user_name = message.from_user.first_name

    # Inline WebApp tugmasi
    inline_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🥟 Menyu & Buyurtma berish (Mini App)",
                    web_app=WebAppInfo(url=WEBAPP_URL),
                )
            ],
            [
                InlineKeyboardButton(
                    text="📞 Aloqa & Manzil",
                    callback_data="contact_info",
                )
            ],
        ]
    )

    # Pastki doimiy menyu tugmasi (Reply Keyboard)
    reply_kb = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="📱 Ilovani ochish",
                    web_app=WebAppInfo(url=WEBAPP_URL),
                )
            ]
        ],
        resize_keyboard=True,
    )

    welcome_text = (
        f"Assalomu alaykum, <b>{user_name}</b>!\n\n"
        "<b>Chustiy Express</b> milliy taomlar yetkazib berish xizmatiga xush kelibsiz! 🇺🇿\n\n"
        "✨ Issiq to'y oshi, lahm shashliklar va tansiq taomlarni "
        "quyidagi qulay <b>Telegram Mini App</b> orqali bir zumda tanlab buyurtma berishingiz mumkin:"
    )

    await message.answer(
        welcome_text,
        reply_markup=inline_kb,
        parse_mode="HTML",
    )
    # Shuningdek doimiy menyu tugmasini o'rnatamiz
    await message.answer(
        "💡 Istalgan vaqtda pastdagi 'Ilovani ochish' tugmasi orqali menyuga kirishingiz mumkin.",
        reply_markup=reply_kb,
    )


@dp.callback_query(F.data == "contact_info")
async def contact_callback(callback: types.CallbackQuery):
    await callback.message.answer(
        "📍 <b>Manzil:</b> Toshkent shahri, Amir Temur shox ko'chasi, 14-uy\n"
        "⏰ <b>Ish vaqti:</b> Har kuni 10:00 dan 23:00 gacha\n"
        "📞 <b>Telefon:</b> +998 71 200-00-00\n"
        "🚀 <b>Yetkazib berish:</b> Shahar bo'ylab 30 daqiqa",
        parse_mode="HTML",
    )
    await callback.answer()


@dp.message(F.web_app_data)
async def web_app_data_handler(message: types.Message):
    """Mini App ichidan yuborilgan buyurtma ma'lumotlarini qabul qilish"""
    raw_data = message.web_app_data.data
    try:
        data = json.loads(raw_data)
        count = data.get("count", 1)
        response_text = (
            "🎉 <b>Buyurtmangiz muvaffaqiyatli qabul qilindi!</b>\n\n"
            f"🛒 Taomlar soni: <b>{count} ta</b>\n"
            "⏳ Taxminiy yetkazish vaqti: <b>25-30 daqiqa</b>\n"
            "🛵 Kuryerimiz tez orada siz bilan bog'lanadi.\n\n"
            "Xaridingiz uchun rahmat!"
        )
    except Exception:
        response_text = "🎉 Buyurtmangiz qabul qilindi! Oshxona tayyorlashni boshladi."

    await message.answer(response_text, parse_mode="HTML")


async def main():
    print("Bot muvaffaqiyatli ishga tushdi...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())