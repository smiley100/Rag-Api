#!/bin/sh
set -e

ollama serve &

echo "⏳ Waiting for Ollama..."
until curl -s http://localhost:11434 > /dev/null; do
  sleep 2
done

echo "📥 Pulling models..."
ollama pull nemotron-mini:latest
ollama pull nomic-embed-text:latest

echo "✅ Ollama ready"
wait
