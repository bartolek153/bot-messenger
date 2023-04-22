from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from io import BytesIO
import logging
from PIL import Image
from queue import Queue
import requests
from telegram.helpers import escape_markdown as escape

import constants
from data.dao import DAO
from helper import *
from telegram_channels import channels


class News:
    def __init__(self) -> None:
        self.dao = DAO.get_instance()
        self.queue = Queue()
        self.execute()

    def execute(self):
        try:
            news = self._get_news()

            if news is None:
                return

            # self._parse(news)
            # self._validate()

            t1 = time.time()

            self._parse(news)
            self._validate()

            t2 = time.time()
            print(f"Time elapsed: {t2-t1:.2f}s")

        except Exception as e:
            logging.error(e)

    def _get_news(self):
        return read_file("home.html")

        for attempt in range(constants.MAX_ATTEMPTS):
            with requests.Session() as ses:
                try:
                    make_request(
                        constants.LOGIN_URL,
                        "POST",
                        session=ses,
                        data=constants.USUARIO,
                    )

                    return make_request(
                        constants.HOME_URL,
                        "GET",
                        session=ses,
                    ).text

                except Exception as e:
                    logging.error(f"An error occurred while making the request: {e}")
                    logging.warn(f"Attempt {attempt+1} failed (_get_news())")
                    time.sleep(constants.INTERVAL_MINUTES)

        else:
            logging.critical("Problems found when trying to get news")
            return None

    def _parse(self, news: str):
        parsed_html = BeautifulSoup(news, features="html.parser")
        div_content = parsed_html.find(id=constants.ID_DIV_NOTICIAS)

        # Unwraps <ul>, <ol> tags
        for tag in div_content.find_all(["ul", "ol", "p", "span", "br"]):
            tag.unwrap()

        # # Replace <li> tags with hyphens
        for tag in div_content.find_all("li"):
            tag.replace_with("* " + tag.text.replace("\n", "").strip())

        ses = requests.Session()
        # write_to_file(str(div_content), "a.html")

        for row in div_content.find_all("div", class_="panel panel-default"):
            title = row.find_next(class_="panel-title").text.replace("\n", "").strip()
            body = row.find_next("div", class_="panel-body panel-collapse collapse")

            _images = []

            # Convert <a> tags to markdown
            # for tag in body.find_all("a"):
            #     url = tag.attrs["href"]
            #     tag.replace_with(f"[{tag.text}]({url})")

            if len(img_tags := body.find_all("img")) > 0:
                # continue

                for img in img_tags:
                    response = make_request(img.attrs["src"], "GET", session=ses)
                    content_bytes = BytesIO(response.content)

                    _images.append(Image.open(content_bytes))

                body = merge_images_vertically(_images)
                _images.clear()
            else:
                # needed to reinstantiate BeautifulSoup 
                # because when trying to unwrap <div> tag,
                # nothing was being returned (empty string only)
                body = BeautifulSoup(str(body), "html.parser")
                body.div.unwrap()
                body = str(body).strip()

            _news_data = {"title": title, "body": body}
            self.queue.put(_news_data)

        self.queue.put(None)

    def _validate(self) -> None:
        while True:
            news_data = self.queue.get()

            if news_data is None:
                break

            try:
                news_data_copy = news_data.copy()
                news_data_copy.pop("body")

                if not self.dao.exists_db(self.dao.news, news_data_copy):
                    self._send(news_data)
                    # self.dao.insert_db(self.dao.news, news_data_copy)

            except Exception as e:
                logging.critical(f"Exception with '{news_data['title']}': {e}")

    def _send(self, data: dict) -> None:
        match type(data["body"]):
            case Image.Image:
                channels.send(
                    constants.NOTICIAS_CHAT_ID,
                    message=data["title"],
                    image=data["body"],
                )
            case str:
                channels.send(
                    constants.NOTICIAS_CHAT_ID,
                    message=f"<strong>{data['title']}</strong>\n\n<i>{data['body']}</i>",
                )
