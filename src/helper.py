"""general usage functions"""

import datetime
import logging
import os
import time

import constants
from logs import logger
from requests import Response, Session


def vm_localtime(hour: int, minute: int = 0) -> str:
    """
    Converts Brazil's specified time to the running machine local time, in HH:mm format.

    Parameters:
        `hour` (int): the hour of the day in Brazil to be converted to local time
        `minute` (int, optional): the minute of the hour in Brazil to be converted to local time, defaults to 0

    Returns:
        str: the local time in HH:mm format
    """

    if hour is None:
        raise Exception("Filling hour argument is mandatory.")

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
    Does not apply when debugging.

    Parameters:
        `func` (callable): the function to wrap

    Returns:
        callable: a wrapped version of the function that only runs on weekdays
    """

    def wrapper(*args, **kwargs):
        if os.getenv("PRODUCTION"):
            today = datetime.datetime.now()
            weekday = today.weekday()

            if not weekday < 5:  # not between monday and friday (0 to 4)
                return

        func(*args, **kwargs)

    return wrapper


def only_business_time(func):
    """
    A decorator that wraps a function and only allows it to run during business hours (9:00 to 20:00).
    Does not apply when debugging.

    Parameters:
        `func` (callable): the function to wrap

    Returns:
        callable: a wrapped version of the function that only runs during business hours
    """

    def wrapper(*args, **kwargs):
        if os.getenv("PRODUCTION"):
            now = datetime.datetime.now().time()

            if not datetime.time(9, 0) <= now <= datetime.time(20, 0):
                return

        return func(*args, **kwargs)

    return wrapper


def make_request(
    url: str, 
    method: str, 
    data=None,
    headers=None,
    params=None,
    session: Session=None) -> Response:
    """
    Placeholder function that makes a request to a specified URL.

    Parameters:
        `session` (object): the session object to use for the request
        `url` (str): the URL to request
        `data` (dict, optional): any data to send with the request, defaults to None

    Returns:
        response object resulted of the request made

    Raises:
        exceptions related to unsuccessful http requests
    """

    if session is None:
        session = Session()

    with session as session:
        response = session.request(
            method=method,
            url=url,
            headers=headers,
            data=data,
            params=params
        )

        if response.ok:
            return response
        else:
            response.raise_for_status()


def write_to_file(content: str, filename: str):
    """
    Designed to store strings with big content in a separate file.

    Parameters:
        `content` (str)
        `filename` (str)
    """
    with open(filename, "w") as file:
        file.write(content)


def append_to_file(content: str, filename: str):
    """
    Appends text to a file. If the file doesn't exists, create a new file.

    Parameters:
        `content` (str)
        `filename` (str)
    """

    with open(filename, "a") as f:
        f.write


def read_file(filename: str) -> str:
    """
    Gets the text of a file.

    Parameters:
        `filename` (str)

    Returns:
        str: content of the file.
    """

    with open(filename, "r") as f:
        return f.read()
