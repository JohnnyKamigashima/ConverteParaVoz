const { PollyClient, SynthesizeSpeechCommand } = require('@aws-sdk/client-polly')
const fs = require('fs')
const path = require('path')
const player = require('play-sound')((opts = {}))
require('dotenv').config({ path: '../.aws/credentials' })
const { promisify } = require('util')
const unlink = promisify(fs.unlink)

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
            const content = await readFileSync(filePath, 'utf8')
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

const aiToken = process.env.OPENAI

// Configura o cliente Polly
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

// Função para fazer a requisição ao ChatGPT e retornar a resposta
async function getChatGPTResponse(question) {
    const apiKey = aiToken // Substitua pela sua chave da OpenAI
    const apiUrl = 'https://api.openai.com/v1/chat/completions'

    const data = {
        model: "gpt-4", // Corrigido para um modelo válido
        messages: [
            { role: "system", content: "Resuma o texto para portugues do Brasil, deixando as ideias claras e mencionando a fonte no final quando houver." },
            { role: "user", content: question }
        ],
        max_tokens: 150, // Limite de tokens da resposta
        temperature: 0.5
    }

    try {
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${apiKey}`
            },
            body: JSON.stringify(data)
        })

        const result = await response.json()
        const chatResponse = result.choices[0].message.content
        return chatResponse
    } catch (error) {
        console.error("Erro ao buscar a resposta do ChatGPT:", error)
        return "Desculpe, houve um erro ao tentar obter a resposta."
    }
}

// Função para converter texto em áudio usando Amazon Polly e tocar no Node.js
async function textToSpeech(text, speed = 'fast') {
    const params = {
        TextType: "ssml", // Informa que estamos usando SSML
        Text: `<speak><prosody rate="${speed}">${text}</prosody></speak>`,
        OutputFormat: "mp3",
        VoiceId: "Camila", // Voz em português brasileiro
        LanguageCode: "pt-BR"
    }

    try {
        const command = new SynthesizeSpeechCommand(params)
        const result = await pollyClient.send(command)
        const audioData = result.AudioStream

        // Caminho temporário para salvar o arquivo de áudio
        const filePath = path.join(__dirname, Math.floor(Math.random() * 10000) + '.mp3')

        // Cria um fluxo de escrita para o arquivo
        const fileStream = fs.createWriteStream(filePath)

        // Escreve o áudio no arquivo
        audioData.pipe(fileStream)

        fileStream.on('finish', () => {
            // Reproduz o arquivo de áudio
            player.play(filePath, (err) => {
                if (err) console.error("Erro ao reproduzir o áudio:", err)
                else {
                    console.log("Reproduzindo áudio...")
                    unlink(filePath) // Deleta o arquivo de áudio
                }
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