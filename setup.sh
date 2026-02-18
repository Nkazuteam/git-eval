#!/usr/bin/env bash
set -e

python -m venv .venv

if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source .venv/Scripts/activate
else
    source .venv/bin/activate
fi

pip install -r requirements.txt

if [ ! -f .env ]; then
    cp .env.example .env
    echo ".env created from .env.example — fill in your values"
fi

echo "Done. Activate with:"
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    echo "  source .venv/Scripts/activate"
else
    echo "  source .venv/bin/activate"
fi
