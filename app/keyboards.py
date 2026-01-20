from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton)

send_message = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Отправить сообщение', callback_data='send_message')]
])

def answer(ticked_id): 
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Ответить", callback_data=f"answer:{ticked_id}")]
    ])