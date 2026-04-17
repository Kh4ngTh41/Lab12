# Deployment Information

## Public URL

```
https://my-agent-7xva.onrender.com
```

## Platform

Render

## Test Commands

### Health Check

```bash
curl https://my-agent-7xva.onrender.com/health
# Expected: {"status":"ok"}
```

### API Test (without authentication - should return 401)

```bash
curl https://my-agent-7xva.onrender.com/ask -X POST \
  -H "Content-Type: application/json" \
  -d '{"user_id":"test","question":"Hello"}'
# Expected: 401 Unauthorized
```

### API Test (with authentication)

```bash
curl -X POST https://my-agent-7xva.onrender.com/ask \
  -H "X-API-Key: user1-secret-key" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"user_001","question":"Hello"}'
# Expected: {"answer":"Hello! How can I help you today?","user_id":"user_001"}
```

### Rate Limiting Test

```bash
for i in {1..22}; do
  curl -s -H "X-API-Key: user1-secret-key" \
    https://my-agent-7xva.onrender.com/ask -X POST \
    -H "Content-Type: application/json" \
    -d '{"user_id":"test","question":"test '$i'"}'
done
# Expected: After 20 requests, returns 429 Rate limit exceeded
```

## Environment Variables Set

| Variable | Value |
|----------|-------|
| `PORT` | 8000 |
| `REDIS_URL` | (Redis connection - Upstash or Render Redis) |
| `AGENT_API_KEY` | user1-secret-key |
| `LOG_LEVEL` | INFO |
| `RATE_LIMIT_PER_MINUTE` | 20 |
| `MONTHLY_BUDGET_USD` | 10 |
| `OPENAI_API_KEY` | (optional - for real LLM) |
| `LLM_MODEL` | gpt-4o-mini |

## Deployment Steps

### Render Deployment

1. Push code to GitHub
2. Go to [render.com](https://render.com)
3. New → Blueprint → Connect GitHub repo
4. Render auto-detects `render.yaml`
5. Click "Apply"
6. Add Redis (Environment → Data → Create Redis Instance)

### Railway CLI Deployment

```bash
npm install -g @railway/cli
railway login
railway init
railway up
railway domain
```

### Docker Deployment

```bash
# Build image
docker build -t my-agent .

# Run container
docker run -p 8000:8000 \
  -e REDIS_URL=redis://host.docker.internal:6379 \
  -e AGENT_API_KEY=user1-secret-key \
  my-agent
```

## Screenshots

*(Add screenshots after deployment)*

- [Deployment dashboard](screenshots/dashboard.png)
- [Service running](screenshots/running.png)
- [API test results](screenshots/test.png)
- [Rate limit test](screenshots/rate-limit.png)
