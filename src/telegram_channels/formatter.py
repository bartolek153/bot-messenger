import emoji
import constants


def emojis(message:str, job: dict):

    EMOJIS = constants.JOB_FIELDS

    for field, detail in job.items():
        if detail:
            message += f"{EMOJIS.get(field, '')} {field}: {detail.capitalize()}; \n"

    # print(emoji.emojize(message_header))

    return message