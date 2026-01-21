from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from app.database.requests import create_ticket, set_root_message_id
import app.keyboards as kb
import os

user = Router()


class MessageToSend(StatesGroup):
    message = State()


@user.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "👋 Здравствуйте!\n\nНажмите <b>«Отправить сообщение»</b> и опишите вашу проблему - сообщение будет передано в поддержку.\n\nКак только поступит ответ, он будет отправлен вам.\n\n↩️ Чтобы продолжить диалог по нему - <b>отвечайте (reply) на сообщения бота</b> с ответом поддержки.\n\n🔥 - сообщение успешно отправлено \n👎 - сообщение не удалось отправить", parse_mode='HTML', reply_markup=kb.send_message
    )

@user.callback_query(F.data == 'send_message')
async def take_message(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(MessageToSend.message)
    await callback.message.answer('Опишите детально вашу проблему или вопрос.\nДля удобства можно прикрепить фото/видео.')

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

    if message.text:
        root_message = await message.bot.send_message(
            chat_id=int(os.getenv('GROUP_ID')),
            text=(f"Новое сообщение #{ticket_id} от {full_name} @{username} (id={user_id})\n\n{text}"),
            reply_markup=kb.close(ticket_id)
        )
        
        await set_root_message_id(pool=db, ticket_id=ticket_id, root_message_id=root_message.message_id)

    else:
        root_message = await message.bot.send_message(
            chat_id=int(os.getenv('GROUP_ID')),
            text=(f"Новое сообщение #{ticket_id} от {full_name} @{username} (id={user_id}) ↓↓↓↓↓↓↓↓"),
            reply_markup=kb.close(ticket_id)
        )
        await set_root_message_id(pool=db, ticket_id=ticket_id, root_message_id=root_message.message_id)

        await message.bot.copy_message(
            chat_id=int(os.getenv('GROUP_ID')),
            from_chat_id=message.chat.id,
            message_id=message.message_id)

    

    await message.answer(f"✅ Обращение под номером #{ticket_id} отправлено.\nОжидайте ответ.")

    await state.clear()
