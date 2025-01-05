#!/bin/bash

mkdir -p ./data/bronze

# Check if the user has provided an argument
if [ $# -eq 0 ]; then
    echo "Usage: $0 {champions|players|matches}"
    exit 1
fi


echo "Running champions script..."
docker run -it -v $(pwd)/data:/app/data riot-api-fetcher python main.py

# Define the valid script names
SCRIPT_NAME=$1

# Check if the argument is one of the valid options
case $SCRIPT_NAME in
    champions)
        echo "Running champions script..."
        docker run -it -v $(pwd)/data:/app/data -v $(pwd)/scripts/champions.py:/app/champions.py riot-api-fetcher python champions.py
        ;;
    players)
        echo "Running players script..."
        docker run -it -v $(pwd)/data:/app/data -v $(pwd)/scripts/players.py:/app/players.py riot-api-fetcher python players.py
        ;;
    matches)
        echo "Running matches script..."
        docker run -it -v $(pwd)/data:/app/data -v $(pwd)/scripts/matches.py:/app/matches.py riot-api-fetcher python matches.py
        ;;
    *)
        echo "Invalid argument. Usage: $0 {champions|players|matches}"
        exit 1
        ;;
esac