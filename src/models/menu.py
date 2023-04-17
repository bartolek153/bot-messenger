from bs4 import BeautifulSoup
from datetime import datetime
import logging
import requests
import time
from typing import Union

import constants
from helper import only_weekday, make_request
from telegram_channels import channels


class Menu:
    def __init__(self) -> None:
        pass

    @only_weekday
    def fetch(self):
        """
        Retrieves the menu, for the current day of the week, and sends it
        to the Telegram channel.

        Runs only on weekdays.
        """

        logging.info("Starting menu execution")
        start = time.time()

        try:
            menu = self._get_menu()

            if menu is None:
                return

            menu = self._extract_info(menu)
            self._send_alert(menu)

            end = time.time()
            elapsed_time = end - start

            return logging.info(f"Menu sent with success ({elapsed_time:.2f}s)")

        except Exception as e:
            logging.error(e)

    def _get_menu(self) -> Union[None, str]:
        """
        Makes a request to get menu HTML.

        Returns:
            str: menu HTML.
        """

        for attempt in range(constants.MAX_ATTEMPTS):
            try:
                with requests.Session() as ses:
                    make_request(
                        constants.LOGIN_URL,
                        "POST",
                        session=ses,
                        data=constants.USUARIO,
                    )

                    return make_request(
                        constants.HOME_URL, "POST", session=ses, data=constants.USUARIO
                    ).text

            except Exception as e:
                logging.error(f"An error occurred while making the request: {e}")
                logging.warn(f"Attempt {attempt+1} failed (_get_menu())")
                time.sleep(constants.INTERVAL_MINUTES)

        else:
            logging.critical("Problems found when trying to get menu")
            return None

    def _extract_info(self, html) -> str:
        """
        Parses the HTML text and extracts the menu referring to the current day.

        Returns:
            str: the menu parsed
        """

        parsed_html = BeautifulSoup(html, features="html.parser")
        div_content = parsed_html.find(id=constants.ID_DIV_CARDAPIO).text

        weekday = datetime.today().weekday()
        weekday_fullname = constants.DIAS_SEMANA.get(weekday)

        if weekday_fullname is None:
            raise Exception("Fullname of dayweek was not registered")

        day_index = div_content.lower().find(weekday_fullname.lower())

        if day_index == -1:
            raise Exception("Couldn't find the meal for the current day")

        meal_index_start = div_content.find("ALMOÇO/JANTAR", day_index)
        meal_index_end = div_content.find("*", meal_index_start)

        if meal_index_end == -1 or meal_index_end == -1:
            raise Exception("Problems when obtaining the menu")

        menu = div_content[meal_index_start:meal_index_end].strip()
        menu += f"\n\n{datetime.today().strftime('%d/%m')}"

        logging.info("Menu parsed with success")

        return menu

    def _send_alert(self, menu) -> None:
        """
        Sends the menu on the channel.

        Args:
            `menu` (str)
        """

        # menu = emoji.emojize(":fork_and_knife_with_plate: ") + menu
        channels.send(chat_id=constants.CARDAPIO_CHAT_ID, message=menu, pin=False)
