import os
import sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import asyncio
import logging
import schedule
import telegram
from telegram_channels import channels as ch, formatter as mf

import constants
from helper import *
from logs import logger
from models.jobs import Job
from models.menu import Menu
from models.news import News

from datetime import datetime


_job = Job()
_menu = Menu()
_news = News()

set_environment("development")

def test_job_execution():
    _job.execute()

def test_menu_execution():
    _menu.execute()

async def test_telegram_bot():
    bot = telegram.Bot(constants.TELEGRAM_API_TOKEN)
    async with bot:
        # print(await bot.get_me())
        print((await bot.get_updates()))

def test_messaging():
    ch.send(constants.VAGAS_CHAT_ID, "teste")

def test_request_helper():
    make_request("asdf", "GET")

# test_job_execution()
# test_menu_execution()
# test_messaging()
test_request_helper()