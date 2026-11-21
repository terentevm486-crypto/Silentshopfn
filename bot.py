import os
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

bot = Bot(token=TOKEN)
dp = Dispatcher()

def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛒 Каталог", callback_data="catalog")],
        [InlineKeyboardButton(text="📦 Мои заказы", callback_data="orders")],
        [InlineKeyboardButton(text="🛟 Поддержка", callback_data="support")]
    ])

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "💜 Добро пожаловать в SILENTSHOPFN!\n\n"
        "Твой Fortnite-магазин. Выбирай нужный раздел:",
        reply_markup=main_menu()
    )

@dp.callback_query(F.data == "catalog")
async def catalog(callback):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💎 V-Bucks", callback_data="vbucks")],
        [InlineKeyboardButton(text="👤 Аккаунты", callback_data="accounts")],
        [InlineKeyboardButton(text="🎁 Подписки", callback_data="subscriptions")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back")]
    ])
    await callback.message.edit_text(
        "🛒 КАТАЛОГ SILENTSHOPFN\n\nВыбери категорию:",
        reply_markup=keyboard
    )
    await callback.answer()

@dp.callback_query(F.data.in_({"vbucks", "accounts", "subscriptions"}))
async def empty_category(callback):
    await callback.answer("Скоро здесь появятся товары!", show_alert=True)

@dp.callback_query(F.data == "orders")
async def orders(callback):
    await callback.answer("Пока у тебя нет заказов.", show_alert=True)

@dp.callback_query(F.data == "support")
async def support(callback):
    await callback.message.answer("🛟 Напиши администратору магазина.")
    await callback.answer()

@dp.callback_query(F.data == "back")
async def back(callback):
    await callback.message.edit_text(
        "💜 SILENTSHOPFN\n\nВыбирай нужный раздел:",
        reply_markup=main_menu()
    )
    await callback.answer()

async def main():
    if not TOKEN:
        raise RuntimeError("Не задан BOT_TOKEN!")
    await dp.start_polling(bot)

if name == "main":
    asyncio.run(main())
