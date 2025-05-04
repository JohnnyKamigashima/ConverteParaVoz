FROM python:3.9-slim

WORKDIR /app
COPY . .

RUN apt-get update && apt-get install -y inotify-tools && apt-get clean

RUN pip install -r requirements.txt

RUN chmod +x converte_para_voz.zsh

