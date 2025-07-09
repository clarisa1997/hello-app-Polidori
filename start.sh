#!/bin/bash

echo "Avvio progetto hello-app..."

# Verifica Docker
if ! command -v docker &> /dev/null; then
    echo "Docker non è installato. Installalo prima di continuare."
    exit 1
fi

# Verifica Docker Compose
if ! command -v docker compose &> /dev/null; then
    echo "docker compose non è installato. Installalo o usa Docker Desktop."
    exit 1
fi

# Verifica Make
if ! command -v make &> /dev/null; then
    echo "Make non è installato. Userò docker compose manualmente."
    echo "Eseguo: docker compose up --build -d"
    docker compose up -d --build
else
    echo "Eseguo: make build && make up"
    make build && make up
fi

echo "Applicazione in esecuzione su: http://localhost:8000"
