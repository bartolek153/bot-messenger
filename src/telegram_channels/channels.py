import asyncio
import telegram
from telegram.helpers import escape_markdown
from telegram.constants import ParseMode

import constants


def send(chat_id, message, pin=False, mode=ParseMode.HTML):
    asyncio.run(_send_message_api(chat_id, message, pin, mode))


async def _send_message_api(chat_id, message, pin, mode):
    bot = telegram.Bot(constants.TELEGRAM_API_TOKEN)

    if mode == ParseMode.MARKDOWN:
        message = escape_markdown(message, version=2)

    async with bot:

        result = await bot.send_message(
            text=message, 
            chat_id=chat_id, 
            parse_mode=mode
        )

        if pin:
            await bot.unpin_all_chat_messages(chat_id=chat_id)
            await bot.pin_chat_message(
                chat_id=chat_id, 
                message_id=result.message_id, 
                disable_notification=True
            )
