import os
import asyncio
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import ADMIN_ID
from services import system

router = Router()
router.message.filter(F.from_user.id == ADMIN_ID)
ADMIN_ID = int(os.getenv("ADMIN_ID"))

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("🛠 Система мониторинга Zero-Home активна.")

@router.message(Command("admin"))
async def admin_panel(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="📊 Статус", callback_data="st_status"))
    builder.row(types.InlineKeyboardButton(text="🔋 Включить ПК", callback_data="st_wol"))
    builder.row(types.InlineKeyboardButton(text="🔄 Ребут сервера", callback_data="st_reboot"))
    await message.answer("Выберите действие:", reply_markup=builder.as_markup())

@router.callback_query(F.data.startswith("st_"))
async def callbacks(callback: types.CallbackQuery):
    action = callback.data.split("_")[1]

    if action == "status":
        info = system.get_system_info()
        await callback.message.answer(info)
    elif action == "wol":
        res = system.wake_pc()
        await callback.answer(res, show_alert=True)
    elif action == "reboot":
        await callback.message.answer("♻️ Сервер перезагружается...")
        system.reboot_server()
    await callback.answer()

@router.message(F.text == "/shutdown", F.from_user.id == ADMIN_ID)
async def cmd_shutdown(message: types.Message):
    await message.answer("⚠️ Получена команда на выключение. Сервер завершает работу...")
    await asyncio.sleep(3)
    os.system("sudo /usr/sbin/poweroff now")
