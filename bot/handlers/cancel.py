from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.keyboards.menus import main_menu_kb

router = Router()


@router.callback_query(F.data == "cancel")
async def cancel_action(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.answer("❌ Действие отменено.", reply_markup=main_menu_kb())  # type: ignore[union-attr]
    await callback.answer()


@router.callback_query(F.data == "back")
async def back_action(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.answer("◀️ Назад в меню", reply_markup=main_menu_kb())  # type: ignore[union-attr]
    await callback.answer()
