import base64
import logging

# from concurrent.futures import ThreadPoolExecutor, TimeoutError
from io import BytesIO
from queue import Queue

import requests
from bs4 import BeautifulSoup
from PIL import Image

import constants
from data.dao import DAO
from helper import *
from telegram_channels import channels


class News:
    def __init__(self) -> None:
        self.dao = DAO.get_instance()
        self.queue = Queue()

        if self.dao.is_first_execution(self.dao.news):
            self.execute(True)

    def execute(self, first_execution=False):
        try:
            news = self._get_news()

            if news is None:
                return

            t1 = time.time()

            self._parse(news)
            self._validate(first_execution)

            t2 = time.time()
            print(f"Time elapsed: {t2-t1:.2f}s")

        except Exception as e:
            logging.error(e)

    def _get_news(self):
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

        _EXCLUDE_TAGS = ["ul", "ol", "p", "span", "br", "h1"]

        for tag in div_content.find_all(_EXCLUDE_TAGS):
            tag.unwrap()

        # # Replace <li> tags with hyphens
        for tag in div_content.find_all("li"):
            tag.replace_with("* " + tag.text.replace("\n", "").strip())

        ses = requests.Session()

        for row in div_content.find_all("div", class_="panel panel-default"):
            title = row.find_next(class_="panel-title").text.replace("\n", "").strip()

            if self.dao.contains_db(self.dao.news, self.dao.query.title, title):
                continue

            body = row.find_next("div", class_="panel-body panel-collapse collapse")

            _images = []

            if len(img_tags := body.find_all("img")) > 0:
                for img in img_tags:
                    src = img.attrs["src"]
                    image_bytes = BytesIO()

                    # image src is a base64 string, then decode it
                    if src.startswith("data:image"):
                        decoded_data = base64.b64decode(img["src"].split(",")[1])
                        image_bytes.write(decoded_data)

                    # if src attribute is a uri, make a request to get the image
                    elif src.startswith("http"):
                        response = make_request(img.attrs["src"], "GET", session=ses)
                        image_bytes.write(response.content)

                    else:
                        continue

                    _images.append(Image.open(image_bytes))

                body = merge_images_vertically(_images)
                _images.clear()

            # Telegram does not support <table> tags
            elif len(body.find_all("table")) > 0:
                continue

            else:
                # needed to reinstantiate BeautifulSoup
                # because when trying to unwrap <div> tag,
                # nothing was being returned (empty string only)
                body = BeautifulSoup(str(body), "html.parser")
                body.div.unwrap()
                body = str(body).strip()

            _news_data = {"title": title, "body": body}
            self.queue.put(_news_data)

        # self.queue.put(None)

    def _validate(self, first_exec) -> None:
        try:
            if first_exec:
                while not self.queue.empty():
                    news_data = self.queue.get()

                    # if news_data is None:
                    #     break

                    news_data.pop("body")
                    self.dao.insert_db(self.dao.news, news_data)

            else:
                while not self.queue.empty():
                    news_data = self.queue.get()

                    # if news_data is None:
                    #     break

                    news_data_copy = news_data.copy()
                    news_data_copy.pop("body")

                    # if not self.dao.exists_db(self.dao.news, news_data_copy):

                    self._send(news_data)
                    self.dao.insert_db(self.dao.news, news_data_copy)

        except Exception as e:
            logging.critical(f"Exception in '{news_data['title']}': {e}")

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
