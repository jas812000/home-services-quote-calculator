#!/bin/bash
set -e

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_ROOT"

if [ ! -d ".venv" ]; then
    echo "Error: .venv does not exist."
    echo "Create the virtual environment and install development dependencies first."
    exit 1
fi

source .venv/bin/activate
python -m pytest
