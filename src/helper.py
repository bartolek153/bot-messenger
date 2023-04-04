"""general usage functions"""

import datetime
import logging
import os
import time

import constants
from logs import logger
from requests import Response


def vm_localtime(hour: int, minute: int = 0) -> str:
    """
    Converts Brazil's specified time to the running machine local time, in HH:mm format.

    Parameters:
        `hour` (int): the hour of the day in Brazil to be converted to local time
        `minute` (int, optional): the minute of the hour in Brazil to be converted to local time, defaults to 0

    Returns:
        str: the local time in HH:mm format
    """

    if hour == None:
        raise Exception("Filling hour argument is mandatory.")

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

    return local_time.strftime("%H:%M")


def only_weekday(func):
    """
    A decorator that wraps a function and only allows it to run if it's a weekday (Monday to Friday).

    Parameters:
        `func` (callable): the function to wrap

    Returns:
        callable: a wrapped version of the function that only runs on weekdays
    """

    def wrapper(*args, **kwargs):
        today = datetime.datetime.now()
        # Retorna um número entre 0 e 6, sendo 0 segunda-feira e 6 domingo
        weekday = today.weekday()

        if weekday < 5:  # Se for segunda a sexta-feira (0 a 4)
            return func(*args, **kwargs)
        else:
            print("weekend")

    return wrapper


def only_business_time(func):
    """
    A decorator that wraps a function and only allows it to run during business hours (9:00 to 20:00).

    Parameters:
        `func` (callable): the function to wrap

    Returns:
        callable: a wrapped version of the function that only runs during business hours
    """

    def wrapper(*args, **kwargs):
        now = datetime.datetime.now().time()

        if datetime.time(9, 0) <= now <= datetime.time(20, 0):
            return func(*args, **kwargs)

    return wrapper


def make_request(url, method, session=None, data=None) -> Response:
    """
    Placeholder function that makes a request to a specified URL.

    Parameters:
        `session` (object): the session object to use for the request
        `url` (str): the URL to request
        `data` (dict, optional): any data to send with the request, defaults to None

    Returns:
        response object resulted of the request made
    """

    try:
        with session:
            if data:
                return session.get(url, data)
            else:
                return session.get(url)
    except Exception as e:
        logging.error(f"An error occurred while making a request: {e}")
        return None


def write_to_file(content, filename):
    """
    Designed to store strings with big content in a separate file.

    Parameters:
        `content` (str)
        `filename` (str)
    """
    with open(filename, "w") as file:
        file.write(content)


def append_to_file(content, filename):
    """
    Appends text to a file. If the file doesn't exists, create a new file.

    Parameters:
        `content` (str)
        `filename` (str)
    """

    with open(filename, "a") as f:
        f.write


def read_file(filename) -> str:
    """
    Gets the text of a file.

    Parameters:
        `filename` (str)

    Returns:
        str: content of the file.
    """

    with open(filename, "r") as f:
        return f.read()


def set_environment(environment):
    """
    Sets variables and some settings based on the specified environment.

    Parameters:
        `environment` (str): the name of the environment to set

    Raises:
        Exception: if the specified environment is invalid
    """

    if environment == "development":
        constants.VAGAS_CHAT_ID = constants.CARDAPIO_CHAT_ID = constants.NOTICIAS_CHAT_ID = (
            "-1001869822416"
        )

        logger.register_development_logger()
        logging.warn("Running in DEVELOPMENT mode")

    elif environment == "production":
        constants.VAGAS_CHAT_ID = "-1001909104760"
        constants.CARDAPIO_CHAT_ID = "-1001663438555"
        # constants.NOTICIAS_CHAT_ID = ""

        logger.register_production_logger()
        logging.warn("Running in PRODUCTION mode!")

    else:
        raise Exception(f"Problems setting {environment} environment.")
