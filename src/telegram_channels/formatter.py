import emoji
from telegram.helpers import escape_markdown

import constants


def enhance(message: str, job: dict) -> str:
    EMOJIS = constants.JOB_FIELDS

    for field, detail in job.items():
        if detail:
            message += f"{EMOJIS.get(field, '')} <i><b>{field}</b></i>: {detail}\n\n"

    return emoji.emojize(message)
