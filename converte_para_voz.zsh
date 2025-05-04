# export PATH=/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin
# cd "$(dirname "$0")"
# poetry shell
# poetry install
# python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

while true
do
    python converte_para_voz.py
    sleep 5
done