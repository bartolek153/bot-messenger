import asyncio
import aiohttp
from bs4 import BeautifulSoup
from datetime import datetime
import logging

import constants
from helper import only_weekday
from telegram_channels import channels as ch


class Menu:
    def __init__(self):
        pass

    @only_weekday
    def execute(self):
        """
        Retrieves the menu, for the current day of the week, and sends it
        to the Telegram channel.

        Runs on weekdays.
        """

        logging.info("Starting menu execution")

        try:
            menu = asyncio.run(self.get_menu())

            if menu is None:
                return

            menu = self.extract_info(menu)
            self.send_alert(menu)
            logging.info("Menu sent with success")

        except Exception as e:
            logging.exception(e)
            return

    async def get_menu(self) -> str:
        """
        Makes a request to get menu HTML.
        """

        for attempt in range(constants.MAX_ATTEMPTS):

            async with aiohttp.ClientSession() as ses:
                await ses.post(constants.LOGIN_URL, data=constants.USUARIO)
                menu = await ses.get(constants.HOME_URL)

                if menu.ok:
                    return await menu.text()
                else:
                    logging.warn(
                        f"Attempt {attempt+1} failed (get_menu() - code {menu.status})"
                    )
                    await asyncio.sleep(constants.INTERVAL_MINUTES)

        else:
            logging.critical("Problems found when trying to get jobs")
            return None

    def extract_info(self, html):
        """
        Parses the HTML text and extracts the menu referring to the current day.

        Returns:
            str: the menu parsed
        """
        parsed_html = BeautifulSoup(html, features="html.parser")
        div_content = parsed_html.find(id=constants.ID_DIV_CARDAPIO).text

        weekday = datetime.today().weekday()
        weekday_fullname = constants.DIAS_SEMANA.get(weekday)

        day_index = div_content.lower().find(weekday_fullname.lower())
        meal_index_start = div_content.find("ALMOÇO/JANTAR", day_index)
        meal_index_end = div_content.find("*", meal_index_start)

        menu = div_content[meal_index_start:meal_index_end].strip()
        menu += f"\n\n{datetime.today().strftime('%d/%m')}"

        logging.info("Menu obtained with success")

        return menu

    def send_alert(self, menu):
        """
        Sends the menu on the channel.

        Args:
            `menu` (str)
        """
        ch.send(constants.CARDAPIO_CHAT_ID, menu)
