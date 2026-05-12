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

@router.message(Command("shell"), F.from_user.id == ADMIN_ID)
async def shell_command(message: types.Message, command: Command):
    if not command.args:
        return await message.answer("⚠️ Введите команду. Пример: `/shell uptime`", parse_mode="Markdown")
    
    query = command.args
    sent_message = await message.answer(f"⏳ Выполняю: `{query}`...")
    
    try:
        # Выполнение команды в системе
        result = subprocess.check_output(query, shell=True, stderr=subprocess.STDOUT, text=True)
        # Ограничение Telegram на длину сообщения (4096 символов)
        formatted_result = f"
