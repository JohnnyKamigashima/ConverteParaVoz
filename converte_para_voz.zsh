#!/bin/zsh
/opt/homebrew/bin/poetry shell
/opt/homebrew/bin/poetry install
python3 $(pwd)/converte_para_voz.py