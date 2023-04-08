# Usa a imagem oficial do Python como base
FROM python:slim-bullseye

# Define o diretório de trabalho
WORKDIR /app

# Copia o arquivo main.py para dentro do contêiner
COPY . .
COPY requirements.txt .

# Instala as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Executa o arquivo main.py quando o contêiner for iniciado
CMD [ "python", "./src/main.py" ]