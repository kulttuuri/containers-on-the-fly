#!/bin/bash

# Check if the registry container is already running
if [ ! "$(docker ps -q -f name=registry)" ]; then
    if [ "$(docker ps -aq -f status=exited -f name=registry)" ]; then
        # Cleanup any exited registry container
        docker rm registry
    fi
    # Start the Docker registry container
    docker run -d -p 5000:5000 --restart=always --name registry registry:2
fi
