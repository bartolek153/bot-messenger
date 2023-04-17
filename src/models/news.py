from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, wait
from io import BytesIO
import logging
from PIL import Image
from queue import Queue
import requests

import constants
from data.dao import DAO
from helper import *


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

            with ThreadPoolExecutor() as executor:
                # submit the jobs to the executor
                _t1 = executor.submit(self._parse, news)
                _t2 = executor.submit(self._validate)

                # wait for both futures to complete
                wait([_t1, _t2])

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

        # Replace <b> and <strong> tags with asterisks
        for tag in div_content.find_all(["b", "strong"]):
            tag.replace_with("*" + tag.text.replace("\n", "").strip() + "*")

        # Replace <i> tags with asterisks
        for tag in div_content.find_all("i"):
            tag.replace_with("_" + tag.text.replace("\n", "").strip() + "_")

        # Replace <u> tags with underscores
        for tag in div_content.find_all("u"):
            tag.replace_with(" __ " + tag.text.replace("\n", "").strip() + " __ ")

        # Replace <li> tags with hyphens
        for tag in div_content.find_all("li"):
            tag.replace_with("- " + tag.text.replace("\n", "").strip())

        ses = requests.Session()
        # write_to_file(str(div_content), "a.html")

        for row in div_content.find_all("div", class_="panel panel-default"):
            title = row.find_next(class_="panel-title").text.replace("\n", "").strip()
            body = row.find_next("div", class_="panel-body")
            _images = []

            # Convert <a> tags to markdown
            for tag in body.find_all("a"):
                url = tag.attrs["href"]
                tag.replace_with(f"[{tag.text}]({url})")

            if len(img_tags := body.find_all("img")) > 0:
                # continue

                for img in img_tags:
                    response = make_request(img.attrs["src"], "GET", session=ses)
                    content_bytes = BytesIO(response.content)

                    _images.append(Image.open(content_bytes))

                body = merge_images_vertically(_images)
                _images.clear()
            else:
                body = body.text.strip()

            # print(body)
            # print("____")

            _news_data = {"title": title, "body": body}

            self.queue.put(_news_data)
            print("put")
        self.queue.put(None)

        print("Done")

    def _validate(self):
        while True:
            news_data = self.queue.get()
            print("get")

            if news_data is None:
                break

            copy_data = news_data.copy()
            copy_data.pop("body")

            if not self.dao.exists_db(self.dao.news, copy_data):
                self._send()
                self.dao.insert_db(self.dao.news, copy_data)

        print("Done")

    def _send(self):
        raise NotImplementedError()
