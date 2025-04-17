#!/bin/bash

while true; do
  echo ">> Simulação de requisições iniciada..."

  curl -s http://localhost:5000/ > /dev/null
  curl -s http://localhost:5000/health > /dev/null
  curl -s http://localhost:5000/metrics > /dev/null

  for i in {1..3}; do
    curl -s -o /dev/null -w "%{http_code}\n" http://localhost:5000/fail
  done

  echo ">> Requisições feitas, aguardando 10 segundos..."
  sleep 10
done
