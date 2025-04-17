#!/bin/bash

while true; do
  curl -s http://localhost:5000/ > /dev/null
  curl -s http://localhost:5000/history > /dev/null
  curl -s http://localhost:5000/health > /dev/null

  # A cada 10 ciclos, simula uma falha para gerar erro 500
  ((i++))
  if (( i % 10 == 0 )); then
    curl -s http://localhost:5000/fail > /dev/null
  fi

  sleep 2
done
