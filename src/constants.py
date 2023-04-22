import os
import configparser

_config = configparser.ConfigParser()
_config.read("credentials.ini")

# URLs

HOST = "https://aluno.cefsa.edu.br"
LOGIN_URL = f"{HOST}/Login/Login"
HOME_URL = f"{HOST}/Home"
VAGAS_URL = f"{HOST}/VagaEstagio/Pesquisar"


# user credentials to access the website

USUARIO = {
    "Usuario": _config["Portal"]["User"],
    "Senha": _config["Portal"]["Password"]
}


# telegram api keys and chat ids

TELEGRAM_API_TOKEN = _config["Telegram"]["Token"]
USE_EMOJIS = _config["Telegram"]["UseEmojis"]

CARDAPIO_CHAT_ID = ""
VAGAS_CHAT_ID = ""
NOTICIAS_CHAT_ID = ""


# program constants

MAX_ATTEMPTS = int(_config["GET Behavior"]["Attempts"])
INTERVAL_MINUTES = int(_config["GET Behavior"]["Interval"])

""" Menu consts """
ID_DIV_CARDAPIO = "colapseCardapioSemanal"
DIAS_SEMANA = {
    0: "Segunda-feira",
    1: "Terça-feira",
    2: "Quarta-feira",
    3: "Quinta-feira",
    4: "Sexta-feira",
}

""" Jobs consts """
LIMIT_JOBS_PER_FETCH = 5
JOB_FIELDS = {
    "Data do Cadastro": ":calendar:",
    "Empresa": ":office_building:",
    "Cargo": ":briefcase:",
    "Tipo": ":label:",
    "Local": ":round_pushpin:",
    "Requisitos": ":check_mark_button:",
    "Benefícios": ":money_bag:",
    "Descrição": ":clipboard:",
    "Observações": ":pushpin:"
}

""" News consts """
ID_DIV_NOTICIAS = "colapseQuadroAvisos"
LIMIT_NEWS_PER_FETCH = 3
