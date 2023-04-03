"""general usage functions"""

import datetime
from logs import logger
import logging
import os
import time

import constants


def vm_localtime(hour: int, minute: int = 0) -> str:
    """
    Converts Brazil's specified time to the running machine local time, in HH:mm format.

        Parameters:
            hour (int)
            minute (int) -- default is 0

        Returns:
            local time (string)
    """

    if hour == None:
        raise Exception("Filling hour is mandatory.")

    # Create a datetime object representing the given time in Brazil
    brazil_time = datetime.datetime.combine(
        datetime.datetime.today(), datetime.time(hour=hour, minute=minute)
    )

    # Get the local timezone's offset from UTC in seconds
    local_offset = -time.timezone if time.localtime().tm_isdst == 0 else -time.altzone

    # Create a timezone object for the local timezone of the virtual machine
    local_tz = datetime.timezone(datetime.timedelta(seconds=local_offset))

    # Convert the Brazil time to the local timezone of the virtual machine
    local_time = brazil_time.replace(
        tzinfo=datetime.timezone(datetime.timedelta(hours=-3))
    ).astimezone(local_tz)

    # Print the result
    # print(local_time.strftime('%H:%M'))

    return local_time.strftime("%H:%M")


def only_weekday(func):
    def wrapper(*args, **kwargs):
        today = datetime.datetime.now()
        weekday = today.weekday() # Retorna um número entre 0 e 6, sendo 0 segunda-feira e 6 domingo
        
        if weekday < 5: # Se for segunda a sexta-feira (0 a 4)
            return func(*args, **kwargs)
        else:
            print("weekend")

    return wrapper


def only_business_time(func):
    def wrapper(*args, **kwargs):
        now = datetime.datetime.now().time()

        if datetime.time(9, 0) <= now <= datetime.time(20, 0):
                return func(*args, **kwargs)
        else:
            print("time not allowed")

    return wrapper


async def fetch():
    pass


def set_environment(environment):
    # environment = os.environ.get("ENV")

    if environment == "development":
        constants.VAGAS_CHAT_ID = constants.CARDAPIO_CHAT_ID = constants.NOTICIAS_CHAT_ID = (
            "-1001869822416"
        )

        logger.register_development_logger()
        logging.warn("running in development mode")       

    elif environment == "production":
        constants.VAGAS_CHAT_ID = "-1001909104760" 
        constants.CARDAPIO_CHAT_ID = "-1001663438555" 
        # constants.NOTICIAS_CHAT_ID = ""

        logger.register_production_logger()
        logging.warn("running in PRODUCTION mode!")

    else:
        raise Exception(f"Problems setting {environment} environment.")