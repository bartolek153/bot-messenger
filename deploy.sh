#!/bin/bash

echo "Cloning repository..."
git clone -b main https://github.com/bartolek153/bot-messenger.git

cp credentials.ini bot-messenger/
cd bot-messenger

echo "Curent version of the script: $(git describe --abbrev=0 --tags)"

IMAGE_NAME=bot-messenger:$(git describe --abbrev=0 --tags)

echo "Building container..."
docker build -t $IMAGE_NAME .

echo ">> Enter a name for the container instance: "
read INSTANCE_NAME

if docker ps --filter "name=${INSTANCE_NAME}" --format '{{.Names}}' | grep -q "${INSTANCE_NAME}"; then
    echo "Stoping current \"${INSTANCE_NAME}\" container instance..."
    docker stop $INSTANCE_NAME
fi

echo "Starting new container..."
docker run -d --rm -v $(pwd):/app --name $INSTANCE_NAME $IMAGE_NAME

echo "Final size of the container: $(docker images $IMAGE_NAME --format "{{.Size}}")"