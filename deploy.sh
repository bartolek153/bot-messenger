git clone -b main https://github.com/bartolek153/bot-messenger.git

cp credentials.ini bot-messenger/
cd bot-messenger

IMAGE_NAME=bot-messenger:$(git describe --abbrev=0 --tags)

docker build -t $IMAGE_NAME .
docker run -d --rm -v $(pwd):/app --name bot $IMAGE_NAME