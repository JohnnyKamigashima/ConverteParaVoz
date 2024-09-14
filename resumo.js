const { PollyClient, SynthesizeSpeechCommand } = require('@aws-sdk/client-polly')
const fs = require('fs')
const path = require('path')
// @ts-ignore
const player = require('play-sound')((opts = {}))
require('dotenv').config({ path: '../.aws/credentials' })
const { promisify } = require('util')
const { getChatGPTResponse } = require('./getChatGPTResponse')
const unlink = promisify(fs.unlink)
const ffmpeg = require("fluent-ffmpeg")

// Função para obter todos os arquivos `.cpb` na pasta
async function getFilesInDirectory(directory) {
    try {
        const files = await fs.promises.readdir(directory)
        return files.filter(file => file.endsWith('.cpb'))
    } catch (error) {
        console.error('Erro ao listar arquivos no diretório:', error)
        return []
    }
}

// Função para processar cada arquivo `.cpb`
async function processFilesInDirectory(directory) {
    const files = await getFilesInDirectory(directory)
    const file = files[0]
    // for (const file of files) {
        const filePath = path.join(directory, file)
        try {
            // Lê o conteúdo do arquivo
            const content = await readFileSync(filePath)
            // Processa o arquivo com o conteúdo
            await askChatGPTAndSpeak(content)
            // Deleta o arquivo após processamento
            await unlink(filePath)
            console.log(`Arquivo ${file} processado e excluído.`)
        } catch (error) {
            console.error(`Erro ao processar o arquivo ${file}:`, error)
        }
    // }
}

// Configura o cliente Polly
// @ts-ignore
const pollyClient = new PollyClient({
    region: process.env.region,
    credentials: {
        accessKeyId: process.env.aws_access_key_id,
        secretAccessKey: process.env.aws_secret_access_key,
    },

})

function readFileSync(filePath) {
    try {
        const data = fs.readFileSync(filePath, 'utf8') // 'utf8' para ler o arquivo como string
        console.log(data)
        return data
    } catch (error) {
        console.error('Erro ao ler o arquivo:', error)
    }
}

async function textToSpeech(text) {
    const params = {
        TextType: "text", // Usando texto simples
        Text: text, // Texto a ser sintetizado
        OutputFormat: "mp3",
        VoiceId: "Camila", // Voz em português brasileiro
        LanguageCode: "pt-BR"
    }

    try {
        // @ts-ignore
        const command = new SynthesizeSpeechCommand(params)
        const result = await pollyClient.send(command)
        const audioData = result.AudioStream

        // Caminho temporário para salvar o arquivo de áudio
        const filePath = path.join(__dirname, Math.floor(Math.random() * 10000) + '.mp3')

        // Cria um fluxo de escrita para o arquivo
        const fileStream = fs.createWriteStream(filePath)

        // Escreve o áudio no arquivo
        // @ts-ignore
        audioData.pipe(fileStream)

        fileStream.on('finish', async () => {
            const modified = filePath.replace('.mp3', '_modified.mp3')

            // Aumenta a velocidade de reprodução do áudio para 2x
            ffmpeg(filePath)
                .audioFilter('atempo=1.75') // Aumenta a velocidade para 2x
                .save(modified)
                .on('end', () => {
                    // Reproduz o arquivo de áudio modificado
                    player.play(modified, (err) => {
                        if (err) console.error("Erro ao reproduzir o áudio:", err)
                        else {
                            console.log("Reproduzindo áudio em velocidade 2x...")
                            unlink(filePath) // Deleta o arquivo de áudio modificado
                            unlink(modified) // Deleta o arquivo de áudio 
                                .catch(err => console.error("Erro ao deletar o arquivo:", err))
                        }
                    })
                })
                .on('error', (err) => {
                    console.error("Erro ao modificar o áudio:", err)
                })

        })

        fileStream.on('error', (err) => {
            console.error("Erro ao gravar o áudio no arquivo:", err)
        })

    } catch (error) {
        console.error("Erro ao converter texto para fala usando Polly:", error)
    }
}

// Função principal que faz a pergunta e retorna a resposta em voz
async function askChatGPTAndSpeak(question) {
    const response = await getChatGPTResponse(question)
    console.log("Resposta do ChatGPT:", response)
    await textToSpeech(response) // Convertendo a resposta em voz com Amazon Polly
}

async function main() {
    const directory = __dirname // Define o diretório onde os arquivos `.cpb` estão localizados
    await processFilesInDirectory(directory);

}

// Executa a função main
main().catch(err => console.error("Erro ao executar a função main:", err))

module.exports = { askChatGPTAndSpeak }