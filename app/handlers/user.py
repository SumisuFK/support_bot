from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import app.keyboards as kb
import os

user = Router()

class MessageToSend(StatesGroup):
    message = State()

@user.message(CommandStart())
async def start(message: Message):
    await message.answer("👋 Здравствуйте! \n\nНажмите кнопку <b>'Отправить сообщение'</b>, после чего опишите свою проблему или вопрос — сообщение будет передано в поддержку. \n\nКак только поступит ответ, он будет отправлен вам.", parse_mode='HTML', reply_markup=kb.send_message)













# @user.callback_query(F.data == 'send_message')
# async def take_message(callback: CallbackQuery, state: FSMContext):
#     await callback.answer()
#     await state.set_state(MessageToSend.message)
#     await callback.message.answer('Опишите детально вашу проблему или вопрос.')
    
# @user.message(MessageToSend.message)
# async def send_message(message: Message, state: FSMContext):

#     message_from_user = message.text
#     username = '@' + message.from_user.username
#     user_id = message.from_user.id
#     name = message.from_user.full_name

#     await message.answer('Сообщение передано в поддержку ✅ \nОжидайте ответ.')
#     await message.bot.send_message(chat_id=int(os.getenv('GROUP_ID')), text=f"Пользователь {name} {username} ({user_id}) отправил сообщение: \n{message_from_user}", reply_markup=kb.answer(message.from_user.id, name, message_from_user))
#     await state.clear()