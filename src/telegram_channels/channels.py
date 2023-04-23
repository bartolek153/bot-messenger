import asyncio
from io import BytesIO

from PIL.Image import Image
import telegram
from telegram.constants import ParseMode
from telegram.error import TelegramError
from telegram.helpers import escape_markdown

import constants


def send(chat_id, message, pin=False, mode=ParseMode.HTML, image=None):
    asyncio.run(_send_message_api(chat_id, message, pin, mode, image))


async def _send_message_api(chat_id, message, pin, mode, image):
    bot = telegram.Bot(constants.TELEGRAM_API_TOKEN)

    try:
        async with bot:
            if image:
                io = BytesIO()
                image.save(io, "PNG")
                io.seek(0)

                result = await bot.send_photo(
                    photo=io, chat_id=chat_id, caption=message, parse_mode=mode
                )
            else:
                result = await bot.send_message(
                    text=message, chat_id=chat_id, parse_mode=mode
                )

            if pin:
                await bot.unpin_all_chat_messages(chat_id=chat_id)
                await bot.pin_chat_message(
                    chat_id=chat_id,
                    message_id=result.message_id,
                    disable_notification=True,
                )
    except TelegramError as e:
        raise e
