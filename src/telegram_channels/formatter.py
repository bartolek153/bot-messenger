import emoji
import constants


def emojis(message_header:str, job: dict):

    EMOJIS = constants.JOB_FIELDS

    for field, detail in job.items():
        if detail:
            message_header += f"{EMOJIS.get(field, '')} {field}: {detail.capitalize()}; \n"

    # print(message_header)
    print(emoji.emojize(message_header))
    return message_header