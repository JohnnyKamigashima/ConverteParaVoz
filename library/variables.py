with open('../.openapi_credentials', encoding='utf-8') as f:
    contents = f.read()
API_KEY: str = ''
BOT_TOKEN: str = ''

for line in contents.split('\n'):
    if line.startswith('openai_api_key='):
        API_KEY: str = line[len('openai_api_key='):]
    elif line.startswith('bot_token='):
        BOT_TOKEN: str = line[len('bot_token='):]

# Open api autentication files in ../.openapi_credentials
# api_key=
# api_secret=None

# Amazon Poly credentials in ../.aws/credentials
# [default]
# aws_access_key_id =
# aws_secret_access_key =
# region=us-east-1

# Models: text-davinci-003,text-curie-001,text-babbage-001,text-ada-001
MODEL = 'gpt-4o-mini'

# Defining the bot's personality using adjectives
BOT_PERSONALITY = 'Resuma o texto para português do Brasil, \
     de forma que seja como uma conversa informal, e pontos duplos para pausas.  \
        Detalhe cada idéia mencionada no texto de forma clara e simples que qualquer pessoa leiga consiga entender sem inventar novas idéias nem criar novos sentidos. \
            Se houver trechos de códigos, descreva a funcionalidade do código e o resultado gerado por ele e remova os trechos de código.\
                  Se houver cabeçalhos, indices e outros elementos que sejam irrelevantes para o entendimento do contexto, \
                    remova antes de traduzir. \
                        Não tente acessar links, cite-os como fonte mas nao acesse nem resuma seu conteudo.'

# Define response file
RESPONSE_BASE_FILE = './responses/responseGPT'
CHAT_ID = "-1001899083389"
QUEUE_FILE = 'queue.txt'
AUDIO_EXTENSION = 'mp3'
OUTPUT_FILE = './responses/output'+'.' + AUDIO_EXTENSION
OGG_OUTPUT_FILE = './responses/output'+'.' + 'ogg'
AUDIO_OUTPUT_PATH = './responses/'
TEXTO_INDESEJADO: list[str] = [
    'Reescreva em português do Brasil, corrigindo com pontuação correta para uma melhor leitura',
    'Reescrevendo com pontuação correta:',
    'Reescrevendo em português do Brasil, com a pontuação correta para uma melhor leitura:',
    BOT_PERSONALITY
    ]