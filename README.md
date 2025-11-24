# OpenAI Proxy API

API proxy para interagir com OpenAI Assistants, formatada para ManyChat Dynamic Blocks.

## Recursos

- Integração com OpenAI Assistants
- Formato de resposta compatível com ManyChat Dynamic Block v2
- Suporte a conversas com contexto via `session_id`
- Timeout de 60 segundos (Fly.io)

## Deploy no Fly.io

### 1. Instalar Fly CLI

```bash
# macOS
brew install flyctl

# Linux
curl -L https://fly.io/install.sh | sh

# Windows
powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
```

### 2. Login no Fly.io

```bash
flyctl auth login
```

### 3. Criar e configurar a aplicação

```bash
# Criar app (o nome será gerado automaticamente ou use o do fly.toml)
flyctl launch --no-deploy

# Configurar a secret da OpenAI API Key
flyctl secrets set OPENAI_API_KEY=sua_chave_aqui
```

### 4. Deploy

```bash
flyctl deploy
```

### 5. Verificar status

```bash
flyctl status
flyctl logs
```

## Endpoints

### GET /
Retorna status da API.

**Resposta:**
```json
{
  "Status": "API is running. Use the /chat endpoint to interact."
}
```

### POST /chat

Envia mensagem para o OpenAI Assistant.

**Request:**
```json
{
  "session_id": "thread_abc123",  // Opcional - para continuar conversa
  "assistant_id": "asst_xyz789",  // Obrigatório
  "message": "sua mensagem",       // Obrigatório
  "assunto": "assunto da conversa", // Obrigatório
  "objetivo": "objetivo da interação" // Obrigatório
}
```

**Response (ManyChat Dynamic Block v2):**
```json
{
  "version": "v2",
  "content": {
    "messages": [
      {
        "type": "text",
        "text": "Resposta do assistant"
      }
    ]
  }
}
```

## Configurações

### Timeout
- **Vercel (Free)**: 10 segundos
- **Fly.io (Free)**: 60 segundos ✅

O timeout está configurado em `fly.toml`:
```toml
[http_service.timeouts]
  hard_timeout = "60s"
  idle_timeout = "30s"
```

### Região
Por padrão, a app é deployada em São Paulo (GRU). Para mudar, edite `fly.toml`:
```toml
primary_region = "gru"  # Outras opções: iad, lhr, syd, etc.
```

### Recursos da VM
```toml
[[vm]]
  cpu_kind = "shared"
  cpus = 1
  memory_mb = 256
```

## Deploy alternativo: Vercel

O projeto também pode ser deployado no Vercel (mantido para compatibilidade):

```bash
vercel --prod
```

**Limitação:** Timeout de 10 segundos no plano gratuito.

## Variáveis de Ambiente

- `OPENAI_API_KEY`: Chave da API da OpenAI (obrigatória)
- `PORT`: Porta do servidor (automática no Fly.io)

## Desenvolvimento Local

```bash
# Instalar dependências
pip install -r requirements.txt

# Rodar servidor
uvicorn api.index:app --reload --port 8080

# Testar
curl -X POST http://localhost:8080/chat \
  -H "Content-Type: application/json" \
  -d '{
    "assistant_id": "asst_xxxxx",
    "message": "teste",
    "assunto": "teste",
    "objetivo": "validar"
  }'
```

## Tecnologias

- FastAPI
- OpenAI Python SDK
- Uvicorn
- Docker (para Fly.io)
