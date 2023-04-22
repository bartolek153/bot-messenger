import logging
import os

current_dir = os.path.dirname(os.path.realpath(__file__))

_debug_format = f"%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
_log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
_file_path = os.path.join(current_dir, "app.log")


def get_file_handler():
    file_handler = logging.FileHandler(_file_path)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(_log_format))
    return file_handler


def get_stream_handler():
    stream_handler = logging.StreamHandler()
    # stream_handler.setLevel(logging.DEBUG)
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(logging.Formatter(_debug_format))
    return stream_handler


def register_development_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    logger.handlers = [get_stream_handler()]
    logging.info("Logger active")


def register_production_logger():
    # on production environment, creates a .log file
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    logger.addHandler(get_file_handler())
    logger.addHandler(get_stream_handler())
    logging.info("Logger active")
