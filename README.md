## ConverteParaVoz

Automação em Python para:
- Ler arquivos `.txt` em lote.
- Reescrever/normalizar conteúdo com OpenAI.
- Gerar áudio a partir do texto.
- Concatenar, converter para OGG e enviar para Telegram.
- Limpar arquivos temporários ao final do processamento.

## Requisitos

- Python 3.11+
- FFmpeg disponível no sistema (necessário para `pydub`)
- Credenciais em `../.openapi_credentials` com:
	- `openai_api_key=...`
	- `bot_token=...`

## Instalação

Com Poetry:

```bash
poetry install
```

Ou com pip:

```bash
pip install -r requirements.txt
```

## Execução

```bash
python converte_para_voz.py
```

O processo busca todos os arquivos `.txt` no diretório atual, processa um por vez e remove o arquivo de entrada após concluir o envio.

## Arquitetura (por classe de responsabilidade)

- Orquestração principal:
	- `converte_para_voz.py`
- Geração de resposta:
	- `library/generate_reponse.py`
	- `library/process_response.py`
	- `library/query_openai.py`
	- `library/open_ai.py`
- Texto e arquivos:
	- `library/text.py`
	- `library/remove_emojis.py`
	- `library/adicionar_quebras_de_linha.py`
	- `library/substituir_quebras_de_linha.py`
	- `library/splitString.py`
	- `library/write_response.py`
	- `library/le_arquivo_texto.py`
	- `library/concatenar_arquivos.py`
	- `library/copy_file.py`
	- `library/copy_audio_file.py`
	- `library/remove_files.py`
- Áudio e integrações externas:
	- `library/openai_speak.py`
	- `library/polly_speak.py`
	- `library/PlayHT.py`
	- `library/merge_mp3_files.py`
	- `library/convert_mp3_ogg.py`
	- `library/normalize_audio.py`
	- `library/audio_send.py`
	- `library/telegram_bot.py`
- Configurações:
	- `library/variables.py`

## Melhorias aplicadas

- Tipagem estática adicionada em funções, parâmetros e retornos.
- Nomes de funções e variáveis padronizados para legibilidade.
- Fluxo principal quebrado em funções menores e mais testáveis.
- Uso de `with` para garantir fechamento de arquivos.
- Tratamento de cenários inválidos em utilitários de texto.
- Alias de compatibilidade mantido: `generate_reponse` chama `generate_response`.

## Observações

- `library/PlayHT.py` contém credenciais embutidas no código atualmente. Recomenda-se migrar para variáveis de ambiente.
- O projeto depende de serviços externos (OpenAI, Telegram e opcionalmente Polly/PlayHT); falhas de rede ou credenciais inválidas impactam a execução.
