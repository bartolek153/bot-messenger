import os
import sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import environment
import asyncio
from datetime import datetime
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

environment.set_development()

def test_request_helper():
    make_request()

def test_news_execution():
    _news = News()

def test_job_execution():
    _job = Job()

def test_menu_execution():
    _menu = Menu()
    _menu.fetch()

async def test_telegram_bot():
    bot = telegram.Bot(constants.TELEGRAM_API_TOKEN)
    async with bot:
        # print(await bot.get_me())
        print((await bot.get_updates()))

def test_messaging():
    ch.send(constants.VAGAS_CHAT_ID, 
        "~__ _*testesss*_ __~", 
        False, 
        telegram.constants.ParseMode.MARKDOWN_V2
    )


test_news_execution()
# test_job_execution()
# test_menu_execution()
# test_messaging()
# test_request_helper()