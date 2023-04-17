import logging
import os

if not os.path.exists("credentials.ini"):
    raise Exception("Credentials file is not available")

import constants
from logs import logger


def production_environment():
    """ Sets variables and some settings for production mode """

    if not os.environ.get("PRODUCTION"):
        raise Exception("Set environment variables before running in production mode!")

    constants.VAGAS_CHAT_ID = "-1001909104760"
    constants.CARDAPIO_CHAT_ID = "-1001663438555"
    # constants.NOTICIAS_CHAT_ID = ""

    logger.register_production_logger()
    logging.warn("Running in PRODUCTION mode!")


def development_environment():
    """ Settings for development mode """
        
    if not os.path.exists("credentials.ini"):
        raise Exception("The credentials file is not available")

    # Tests channel
    constants.VAGAS_CHAT_ID = (
    constants.CARDAPIO_CHAT_ID
    ) = constants.NOTICIAS_CHAT_ID = "-1001869822416"

    logger.register_development_logger()
    logging.warn("Running in DEVELOPMENT mode")