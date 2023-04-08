IMAGE_NAME=bot-messenger:$(git describe --abbrev=0 --tags)

docker build -t $IMAGE_NAME .
docker run -d --rm --mount $(pwd):/app $IMAGE_NAME --name telegram-bot