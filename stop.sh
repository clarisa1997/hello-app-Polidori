#!/bin/bash

echo "Arresto progetto hello-app..."

if command -v make &> /dev/null; then
    make down
else
    docker compose down
fi
