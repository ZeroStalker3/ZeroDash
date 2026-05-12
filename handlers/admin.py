import os
import subprocess
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

@router.message(Command("ping"), F.from_user.id == ADMIN_ID)
async def cmd_ping(message: types.Message):
    await message.answer("✅ Бот видит админа и готов к командам!")


@router.message(Command("shell"))
async def cmd_shell(message: types.Message):
    # 1. Проверка прав доступа
    if str(message.from_user.id) != str(ADMIN_ID):
        await message.reply("⛔ У вас нет прав для выполнения этой команды.")
        return

    # 2. Извлекаем команду после /shell
    command = message.text.replace("/shell", "").strip()

    if not command:
        await message.reply("📝 Введите команду после /shell (например: `/shell uptime`)", parse_mode="Markdown")
        return

    # Отправляем сообщение о начале выполнения
    status_msg = await message.answer(f"⏳ Выполняю: `{command}`...", parse_mode="Markdown")
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=15
        )

        output = result.stdout if result.stdout else result.stderr

        if not output or not output.strip():
            await status_msg.edit_text("✅ Команда выполнена, вывод пуст.")
        else:
            final_output = f"Результат:\n<code>{output}</code>"
            await status_msg.edit_text(final_output, parse_mode="Markdown")

    except subprocess.TimeoutExpired:
        await status_msg.edit_text("⏳ Ошибка: Время ожидания (15 сек) истекло.")
        
    except Exception as e:
        await status_msg.edit_text(f"❌ Ошибка выполнения: `{str(e)}`", parse_mode="Markdown")

