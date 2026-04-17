# Production AI Agent

A production-ready AI agent with FastAPI, Docker, and cloud deployment support.

## Features

- **REST API** - FastAPI-based agent that answers questions
- **Authentication** - API key authentication
- **Rate Limiting** - 20 requests/minute per user
- **Cost Guard** - $10/month budget per user
- **Stateless Design** - Redis for session storage
- **Health Checks** - Liveness and readiness probes
- **Docker Ready** - Multi-stage build, < 200MB image
- **Cloud Deploy** - Railway, Render, or GCP Cloud Run

## Quick Start

### Local Development

```bash
# 1. Clone and install dependencies
pip install -r requirements.txt

# 2. Start Redis (using Docker)
docker run -d -p 6379:6379 redis:7-alpine

# 3. Copy environment file
cp .env.example .env

# 4. Run the app
uvicorn app.main:app --reload
```

### Docker Compose

```bash
# Start full stack (agent + redis + nginx)
docker compose up --build

# Scale agent instances
docker compose up --scale agent=3
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Liveness probe |
| `/ready` | GET | Readiness probe (checks Redis) |
| `/token` | POST | Get JWT token |
| `/ask` | POST | Ask question to AI agent |

## Authentication

All API calls require the `X-API-Key` header:

```bash
curl -X POST http://localhost:8000/ask \
  -H "X-API-Key: user1-secret-key" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user_001", "question": "What is Docker?"}'
```

### API Keys

| Key | User ID |
|-----|---------|
| `user1-secret-key` | user_001 |
| `user2-secret-key` | user_002 |
| `admin-secret-key` | admin_001 |

## Configuration

Environment variables (see `.env.example`):

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | 8000 | Server port |
| `REDIS_URL` | redis://localhost:6379 | Redis connection URL |
| `AGENT_API_KEY` | user1-secret-key | Default API key |
| `LOG_LEVEL` | INFO | Logging level |
| `RATE_LIMIT_PER_MINUTE` | 20 | Max requests per minute |
| `MONTHLY_BUDGET_USD` | 10 | Budget per user per month |

## Deployment

### Railway

```bash
npm install -g @railway/cli
railway login
railway init
railway variables set REDIS_URL=<your-redis-url>
railway variables set AGENT_API_KEY=<your-secret-key>
railway up
railway domain
```

### Render

1. Push to GitHub
2. Connect to [Render.com](https://render.com)
3. Create Blueprint with `render.yaml`
4. Set environment variables

## Project Structure

```
my-production-agent/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI app
│   ├── config.py        # Settings
│   ├── auth.py          # API key auth
│   ├── rate_limiter.py  # Rate limiting
│   └── cost_guard.py   # Budget tracking
├── utils/
│   └── mock_llm.py      # Mock LLM responses
├── Dockerfile          # Multi-stage build
├── docker-compose.yml   # Full stack
├── railway.toml        # Railway config
├── requirements.txt    # Python deps
├── .env.example         # Env template
└── .dockerignore
```

## Testing

```bash
# Health check
curl http://localhost:8000/health

# Without auth (should fail)
curl http://localhost:8000/ask

# With auth (should succeed)
curl -X POST http://localhost:8000/ask \
  -H "X-API-Key: user1-secret-key" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user_001", "question": "Hello"}'

# Rate limit test
for i in {1..22}; do
  curl -s -H "X-API-Key: user1-secret-key" \
    http://localhost:8000/ask -X POST \
    -H "Content-Type: application/json" \
    -d '{"user_id":"test","question":"test '$i'"}'
done
```

## License

MIT
# Deploy-Lab12
