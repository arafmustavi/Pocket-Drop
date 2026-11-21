#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/.."
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
pyinstaller --clean --noconfirm pocket_drop.spec
echo "Built: dist/PocketDrop"
