import os


# URLs

HOST = "https://aluno.cefsa.edu.br"
LOGIN_URL = f"{HOST}/Login/Login"
HOME_URL = f"{HOST}/Home"
VAGAS_URL = f"{HOST}/VagaEstagio/Pesquisar"


# User Credentials to access the website

USUARIO = {"Usuario": os.environ["FESA_USER"], "Senha": os.environ["FESA_PASS"]}


# Telegram API keys

TELEGRAM_API_TOKEN = ""

CARDAPIO_CHAT_ID = ""
VAGAS_CHAT_ID = ""
NOTICIAS_CHAT_ID = ""


# Program configs

os.environ["ENV"] = "development"

ID_DIV_CARDAPIO = "colapseCardapioSemanal"
DIAS_SEMANA = {
    0: "Segunda-feira",
    1: "Terça-feira",
    2: "Quarta-feira",
    3: "Quinta-feira",
    4: "Sexta-feira",
}

MAX_ATTEMPTS = 3
INTERVAL_MINUTES = 2 * 60

LIMIT_JOBS_PER_FETCH = 3
