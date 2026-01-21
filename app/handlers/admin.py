from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from app.database.requests import get_ticket, set_status
import app.keyboards as kb
import re
import os

admin = Router()

TICKET_RE = re.compile(r"#(\d+)")

@admin.message(F.reply_to_message)
async def admin_reply(message: Message, db):
    chat_message_id = message.chat.id

    if chat_message_id == int(os.getenv('GROUP_ID')):

        src = message.reply_to_message.text
        m = TICKET_RE.search(src)
        if not m:
            return

        ticket_id = int(m.group(1))
        ticket = await get_ticket(db, ticket_id)

        if not ticket:
            await message.reply("❌ Тикет не найден в БД")
            return

        if ticket["status"] == 'open':

            target_user_id = int(ticket["user_id"])
            admin_name = message.from_user.full_name
            reply_text = message.text

            try:
                await message.bot.send_message(
                    chat_id=target_user_id,
                    text=(
                        f"💬 Ответ от {admin_name} по обращению #{ticket_id}:\n\n{reply_text}"
                    )
                )

            except TelegramForbiddenError:
                # пользователь заблокировал бота
                await message.bot.set_message_reaction(
                    message.chat.id,
                    message.message_id,
                    reaction=[{"type": "emoji", "emoji": "👎"}]
                )

            except TelegramBadRequest as e:
                # некорректный user_id и т.п.
                await message.reply(f"❌ Ошибка отправки: {e.message}")

            else:
                await message.bot.set_message_reaction(
                    message.chat.id,
                    message.message_id,
                    reaction=[{"type": "emoji", "emoji": "🔥"}]
                )
        else:
            await message.bot.set_message_reaction(
                    message.chat.id,
                    message.message_id,
                    reaction=[{"type": "emoji", "emoji": "👎"}]
                )
        
    else:
        src = message.reply_to_message.text
        m = TICKET_RE.search(src)
        if not m:
            return

        ticket_id = int(m.group(1))
        ticket = await get_ticket(db, ticket_id)

        if not ticket:
            await message.reply("❌ Тикет не найден в БД")
            return

        if ticket["status"] == 'open':

            root_message_id = int(ticket["root_message_id"])
            client_name = message.from_user.full_name
            reply_text = message.text
            group_id = int(os.getenv('GROUP_ID'))

            try:
                if message.text:
                    await message.bot.send_message(
                        chat_id=group_id,
                        text=(
                            f"💬 Пользователь {client_name} дополнил тикет #{ticket_id}:\n\n{reply_text}"
                        ),
                        reply_to_message_id=root_message_id
                    )
                else:
                    await message.bot.send_message(
                        chat_id=group_id,
                        text=(
                            f"💬 Пользователь {client_name} дополнил тикет #{ticket_id} ↓↓↓↓↓↓↓↓"
                        ),
                        reply_to_message_id=root_message_id
                    )

                    await message.bot.copy_message(
                        chat_id=int(os.getenv('GROUP_ID')),
                        from_chat_id=message.chat.id,
                        message_id=message.message_id)

            except TelegramForbiddenError:
                # пользователь заблокировал бота
                await message.bot.set_message_reaction(
                    message.chat.id,
                    message.message_id,
                    reaction=[{"type": "emoji", "emoji": "👎"}]
                )

            except TelegramBadRequest as e:
                # некорректный user_id и т.п.
                await message.reply(f"❌ Ошибка отправки: {e.message}")

            else:
                await message.bot.set_message_reaction(
                    message.chat.id,
                    message.message_id,
                    reaction=[{"type": "emoji", "emoji": "🔥"}]
                )
        else:
            await message.bot.set_message_reaction(
                    message.chat.id,
                    message.message_id,
                    reaction=[{"type": "emoji", "emoji": "👎"}]
                )

@admin.callback_query(F.data.startswith('close:'))
async def close_ticket(callback: CallbackQuery, db):
    await callback.answer()

    ticket_status = callback.data.split(':')[0]
    ticket_id = int(callback.data.split(':')[1])
    
    ticket = await get_ticket(db, ticket_id)
    user_id = ticket["user_id"]

    await set_status(db, ticket_id, ticket_status)
    await callback.message.edit_reply_markup(reply_markup=kb.open(ticket_id))

    await callback.message.bot.send_message(chat_id=user_id, text=f"✅ Ваше обращение #{ticket_id} было закрыто.")

@admin.callback_query(F.data.startswith('open:'))
async def close_ticket(callback: CallbackQuery, db):
    await callback.answer()

    ticket_status = callback.data.split(':')[0]
    ticket_id = int(callback.data.split(':')[1])
    
    ticket = await get_ticket(db, ticket_id)
    user_id = ticket["user_id"]

    await set_status(db, ticket_id, ticket_status)
    await callback.message.edit_reply_markup(reply_markup=kb.close(ticket_id))

    await callback.message.bot.send_message(chat_id=user_id, text=f"♻️ Ваше обращение #{ticket_id} снова открыто.")
