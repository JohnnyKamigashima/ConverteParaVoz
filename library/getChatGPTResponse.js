
// Função para fazer a requisição ao ChatGPT e retornar a resposta

async function getChatGPTResponse(question) {
    const apiKey = process.env.OPENAI // Substitua pela sua chave da OpenAI
    const apiUrl = 'https://api.openai.com/v1/chat/completions'

    const data = {
        model: "gpt-4o-mini", // Corrigido para um modelo válido
        messages: [
            { role: "system", content: "Resuma o texto para portugues do Brasil, deixando as ideias claras e mencionando a fonte no final quando houver." },
            { role: "user", content: question }
        ],
        max_tokens: 4000, // Limite de tokens da resposta
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

module.exports = { getChatGPTResponse }