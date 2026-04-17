# Deployment Information

## Public URL

*(To be filled after deployment to Railway/Render)*

```
https://your-agent.railway.app
```

## Platform

Railway / Render / GCP Cloud Run

## Test Commands

### Health Check

```bash
curl https://your-agent.railway.app/health
# Expected: {"status":"ok"}
```

### API Test (without authentication - should return 401)

```bash
curl https://your-agent.railway.app/ask -X POST \
  -H "Content-Type: application/json" \
  -d '{"user_id":"test","question":"Hello"}'
# Expected: 401 Unauthorized
```

### API Test (with authentication)

```bash
curl -X POST https://your-agent.railway.app/ask \
  -H "X-API-Key: user1-secret-key" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"user_001","question":"Hello"}'
# Expected: {"answer":"Hello! How can I help you today?","user_id":"user_001"}
```

### Rate Limiting Test

```bash
for i in {1..22}; do
  curl -s -H "X-API-Key: user1-secret-key" \
    https://your-agent.railway.app/ask -X POST \
    -H "Content-Type: application/json" \
    -d '{"user_id":"test","question":"test '$i'"}'
done
# Expected: After 20 requests, returns 429 Rate limit exceeded
```

## Environment Variables Set

| Variable | Value |
|----------|-------|
| `PORT` | 8000 |
| `REDIS_URL` | (Redis connection string) |
| `AGENT_API_KEY` | user1-secret-key |
| `LOG_LEVEL` | INFO |
| `RATE_LIMIT_PER_MINUTE` | 20 |
| `MONTHLY_BUDGET_USD` | 10 |

## Deployment Steps

### Railway CLI Deployment

```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login
railway login

# 3. Initialize project
railway init

# 4. Set environment variables
railway variables set REDIS_URL=redis://localhost:6379
railway variables set AGENT_API_KEY=user1-secret-key

# 5. Deploy
railway up

# 6. Get public URL
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
