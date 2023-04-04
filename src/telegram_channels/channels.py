import asyncio
import telegram

import constants


def send(chat_id, message):
    asyncio.run(_send_message_api(chat_id, message))    

def pin(chat_id, message):
    asyncio.run()


async def _send_message_api(id, message):
    bot = telegram.Bot(constants.TELEGRAM_API_TOKEN)
    
    async with bot:
        await bot.send_message(text=message, chat_id=id)


async def _pin_message_api(id, message):
    bot = telegram.Bot(constants.TELEGRAM_API_TOKEN)

    async with bot:
        await bot.pin_chat_message(id, "")
