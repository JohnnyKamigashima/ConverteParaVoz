from pathlib import Path
from typing import Final


def _load_credentials_file() -> str:
    credentials_path: Path = Path('../.openapi_credentials')
    if not credentials_path.exists():
        return ''
    return credentials_path.read_text(encoding='utf-8')


def _extract_credentials(file_content: str) -> tuple[str, str]:
    api_key: str = ''
    bot_token: str = ''

    for line in file_content.split('\n'):
        if line.startswith('openai_api_key='):
            api_key = line[len('openai_api_key='):]
        elif line.startswith('bot_token='):
            bot_token = line[len('bot_token='):]

    return api_key, bot_token


_CREDENTIALS_CONTENT: str = _load_credentials_file()
API_KEY, BOT_TOKEN = _extract_credentials(_CREDENTIALS_CONTENT)

# Open api autentication files in ../.openapi_credentials
# api_key=
# api_secret=None

# Amazon Poly credentials in ../.aws/credentials
# [default]
# aws_access_key_id =
# aws_secret_access_key =
# region=us-east-1

# Models: text-davinci-003,text-curie-001,text-babbage-001,text-ada-001
MODEL: Final[str] = 'gpt-4o-mini'

# Defining the bot's personality using adjectives
BOT_PERSONALITY: Final[str] = 'Reescreva o texto para português do Brasil sem adicionar\
                  introduções nem conclusões. Nos trechos de códigos, descreva\
                  a funcionalidade do código e o resultado gerado por ele e \
                  remova os trechos de código. Se houver cabeçalhos, indices e\
                  outros elementos que sejam irrelevantes para o entendimento \
                  do contexto, remova antes de traduzir. Não acesse links,nem \
                  resuma seu conteudo, cite-os como fonte. Mantenha as frases curtas e objetivas para facilitar a leitura.'

# Define response file
RESPONSE_BASE_FILE: Final[str] = './responses/responseGPT'
CHAT_ID: Final[str] = "-1001899083389"
QUEUE_FILE: Final[str] = 'queue.txt'
AUDIO_EXTENSION: Final[str] = 'mp3'
OUTPUT_FILE: Final[str] = './responses/output' + '.' + AUDIO_EXTENSION
OGG_OUTPUT_FILE: Final[str] = './responses/output' + '.' + 'ogg'
AUDIO_OUTPUT_PATH: Final[str] = './responses/'
TEXTO_INDESEJADO: list[str] = [
    'Reescreva em português do Brasil, corrigindo com pontuação correta para uma melhor leitura',
    'Reescrevendo com pontuação correta:',
    'Reescrevendo em português do Brasil, com a pontuação correta para uma melhor leitura:',
    BOT_PERSONALITY
]