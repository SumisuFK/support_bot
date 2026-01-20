from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from app.database.requests import create_ticket
import app.keyboards as kb
import os

user = Router()


class MessageToSend(StatesGroup):
    message = State()


@user.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "👋 Здравствуйте!\n\n"
        "Нажмите кнопку <b>'Отправить сообщение'</b>, "
        "после чего опишите свою проблему или вопрос — "
        "сообщение будет передано в поддержку.\n\n"
        "Как только поступит ответ, он будет отправлен вам.",
        parse_mode='HTML',
        reply_markup=kb.send_message
    )

@user.callback_query(F.data == 'send_message')
async def take_message(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(MessageToSend.message)
    await callback.message.answer(
        'Опишите детально вашу проблему или вопрос.'
    )

@user.message(MessageToSend.message)
async def send_message(message: Message, state: FSMContext, db):
    ticket_id = await create_ticket(
        pool=db,
        user_id=message.from_user.id,
        username=message.from_user.username,
        full_name=message.from_user.full_name,
        text=message.text
    )

    username = message.from_user.username
    full_name = message.from_user.full_name
    user_id = message.from_user.id
    text = message.text

    await message.bot.send_message(
        chat_id=int(os.getenv('GROUP_ID')),
        text=(
            f"Новое сообщение #{ticket_id} от {full_name} "
            f"@{username} (id={user_id})\n\n"
            f"{text}"
        )
    )

    await message.answer(
        f"✅ Обращение под номером #{ticket_id} отправлено.\n"
        "Ожидайте ответ."
    )

    await state.clear()
