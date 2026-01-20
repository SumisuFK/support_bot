from aiogram.types import Message
from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from app.database.requests import get_ticket
import re
import os

admin = Router()

TICKET_RE = re.compile(r"#(\d+)")

@admin.message(F.reply_to_message)
async def admin_reply(message: Message, db):
    user_channel_status = await message.bot.get_chat_member(
        chat_id=int(os.getenv("GROUP_ID")),
        user_id=message.from_user.id
    )

    if user_channel_status.status == 'left':
        return

    src = message.reply_to_message.text
    m = TICKET_RE.search(src)
    if not m:
        return

    ticket_id = int(m.group(1))
    ticket = await get_ticket(db, ticket_id)

    if not ticket:
        await message.reply("❌ Тикет не найден в БД")
        return

    target_user_id = int(ticket["user_id"])
    admin_name = message.from_user.full_name
    reply_text = message.text

    try:
        await message.bot.send_message(
            chat_id=target_user_id,
            text=(
                f"💬 Ответ от {admin_name}\n"
                f"По обращению #{ticket_id}:\n\n"
                f"{reply_text}"
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
