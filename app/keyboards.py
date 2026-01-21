from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton)
from app.database.requests import get_ticket

send_message = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Отправить сообщение', callback_data='send_message')]
])

def close(ticket_id): 
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Закрыть", callback_data=f"close:{ticket_id}")]
    ])

def open(ticket_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Открыть", callback_data=f"open:{ticket_id}")]
    ])