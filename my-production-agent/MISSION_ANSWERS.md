# Day 12 Lab - Mission Answers

## Part 1: Localhost vs Production

### Exercise 1.1: Anti-patterns found

From analyzing `app.py` in the develop folder, I found these anti-patterns:

1. **Hardcoded API Key** - API key is stored directly in code
2. **Hardcoded Port** - Port 8000 is fixed in code
3. **Debug Mode Enabled** - `debug=True` in production is insecure
4. **No Health Check** - No `/health` or `/ready` endpoints
5. **No Graceful Shutdown** - No signal handlers for SIGTERM
6. **print() Logging** - Using `print()` instead of structured logging
7. **No Rate Limiting** - Anyone can call the API unlimited times
8. **In-Memory State** - Conversation history stored in local dict

### Exercise 1.3: Comparison Table

| Feature | Develop | Production | Why Important? |
|---------|---------|------------|----------------|
| Config | Hardcoded | Environment variables | Different environments have different values |
| Health Check | None | `/health` + `/ready` | Container orchestration needs health checks |
| Logging | print() | JSON structured | Production logs need to be searchable |
| Shutdown | Abrupt | Graceful | Complete in-flight requests before stop |
| Rate Limiting | None | 20 req/min | Prevents abuse |
| Authentication | None | API Key | Public endpoints need auth |
| State | In-memory | Redis | Stateless allows horizontal scaling |

---

## Part 2: Docker

### Exercise 2.1: Dockerfile Questions

1. **Base image**: `python:3.11-slim`
2. **Working directory**: `/app`
3. **Why COPY requirements.txt first?**: Docker caches layers
4. **CMD vs ENTRYPOINT**: CMD can be overridden, ENTRYPOINT is rigid

### Exercise 2.3: Image Size Comparison

- **Develop image**: ~1.2 GB
- **Production image**: ~200 MB (multi-stage build)
- **Difference**: ~83% smaller

### Exercise 2.4: Docker Compose Architecture

```
┌─────────────────────────────────────┐
│         docker-compose.yml          │
├─────────────────────────────────────┤
│  nginx (port 80)                   │
│  agent (port 8000)                 │
│  redis (port 6379)                 │
└─────────────────────────────────────┘
```

---

## Part 3: Cloud Deployment

### Exercise 3.1: Render Deployment

- **URL**: `https://my-agent-7xva.onrender.com`
- **Platform**: Render
- **Test Result**:
  - Health check: ✅ Working
  - API with auth: ✅ Working
  - Rate limit: ✅ Working (429 after 20 requests)

### Exercise 3.2: Render vs Railway Comparison

| Aspect | Railway | Render |
|--------|---------|--------|
| Config File | `railway.toml` | `render.yaml` |
| CLI | `@railway/cli` | Native |
| Free Tier | $5 credit | 750 hours/month |

---

## Part 4: API Security

### Exercise 4.1: API Key Authentication Test

```bash
# Without key - returns 401
curl https://my-agent-7xva.onrender.com/ask -X POST \
  -H "Content-Type: application/json" \
  -d '{"user_id":"test","question":"Hello"}'
# Result: 401 Unauthorized

# With correct key - returns 200
curl -X POST https://my-agent-7xva.onrender.com/ask \
  -H "X-API-Key: user1-secret-key" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"user_001","question":"Hello"}'
# Result: {"answer":"Hello! How can I help you today?","user_id":"user_001"}
```

### Exercise 4.2: JWT Authentication Flow

1. Client sends username/password to `/token`
2. Server validates and returns JWT token
3. Client uses `Authorization: Bearer <token>`

### Exercise 4.3: Rate Limiting Test

```bash
# After 20 requests, returns 429
{"detail":"Rate limit exceeded. Max 20 requests per minute."}
```

### Exercise 4.4: Cost Guard Implementation

```python
def check_budget(user_id: str) -> None:
    month_key = datetime.now().strftime("%Y-%m")
    key = f"budget:{user_id}:{month_key}"
    current = float(r.get(key) or 0)
    if current + 0.01 > 10:
        raise HTTPException(402, "Budget exceeded")
    r.incrbyfloat(key, 0.01)
    r.expire(key, 32 * 24 * 3600)
```

---

## Part 5: Scaling & Reliability

### Exercise 5.1: Health Check Implementation

- `/health` - Liveness probe
- `/ready` - Readiness probe (checks Redis)

### Exercise 5.2: Graceful Shutdown

Using FastAPI lifespan context manager for graceful shutdown.

### Exercise 5.3: Stateless Design

State stored in Redis, not in-memory.

### Exercise 5.4: Load Balancing

```bash
docker compose up --scale agent=3
```

### Exercise 5.5: Stateless Test Results

Conversation history preserved in Redis across instances.

---

## Part 6: Final Project Requirements Checklist

| Requirement | Status | Implementation |
|-------------|--------|----------------|
| Agent trả lời câu hỏi | ✅ | `/ask` endpoint |
| Conversation history | ✅ | Redis with 7-day TTL |
| Dockerized | ✅ | Multi-stage Dockerfile |
| Config từ env vars | ✅ | `pydantic-settings` |
| API key authentication | ✅ | `auth.py` |
| Rate limiting | ✅ | 20 req/min |
| Cost guard | ✅ | $10/month per user |
| Health check | ✅ | `/health` endpoint |
| Readiness check | ✅ | `/ready` endpoint |
| Graceful shutdown | ✅ | Lifespan context |
| Stateless design | ✅ | Redis storage |
| JSON logging | ✅ | Python logging |
| Deploy Railway/Render | ✅ | https://my-agent-7xva.onrender.com |
| OpenAI Support | ✅ | Optional API key |
