FROM python:slim-bullseye
WORKDIR /app

COPY . .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ENV PRODUCTION="enabled"
CMD [ "python", "./src/main.py" ]