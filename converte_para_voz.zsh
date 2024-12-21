
export PATH=/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin
cd "$(dirname "$0")"
poetry shell
poetry install

while true
do
    poetry run python3 converte_para_voz.py
    sleep 5
done