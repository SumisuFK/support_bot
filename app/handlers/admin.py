from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

admin = Router()

class Answer_to_user(StatesGroup):
    message = State()










# @admin.callback_query(F.data.startswith('answer:'))
# async def get_answer_to_message(callback: CallbackQuery, state: FSMContext):
#     user_id = int(callback.data.split(":")[1])
#     name = callback.data.split(":")[2]
#     message_from_user = callback.data.split(":")[3]
#     user_question_id = callback.message.message_id

#     await callback.answer()

#     await state.update_data(user_id = user_id)
#     await state.update_data(user_question_id = user_question_id)
#     await state.update_data(name = name)
#     await state.update_data(message_from_user = message_from_user)

#     text2 = await callback.message.reply("Введите ответ пользователю:")
#     text2_id = text2.message_id
#     await state.update_data(text2_id = text2_id)

#     await state.set_state(Answer_to_user.message)

# @admin.message(Answer_to_user.message)
# async def answer_to_message(message: Message, state: FSMContext):

#     answer = message.text
#     data = await state.get_data()
#     user_id = data["user_id"]
#     answered_name = message.from_user.full_name
#     user_question_id = data["user_question_id"]
#     text2_id = data["text2_id"]
#     messages_to_delete = [user_question_id, text2_id]
#     name = data["name"]
#     message_from_user = data["message_from_user"]


#     await message.delete()
#     await message.bot.delete_messages(chat_id='-1003628078973', message_ids=messages_to_delete)
#     await message.answer(text=f'<b>Вопрос от {name}:</b> {message_from_user}\n<b>Ответ от {answered_name}:</b> {answer}',parse_mode='HTML')
#     await message.bot.send_message(chat_id=user_id, text=f'Пришёл ответ от {answered_name}: \n{answer}')
#     await state.clear()