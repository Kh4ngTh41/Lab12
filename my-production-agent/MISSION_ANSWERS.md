# Day 12 Lab - Mission Answers

## Part 1: Localhost vs Production

### Exercise 1.1: Anti-patterns found

From analyzing `app.py` in the develop folder, I found these anti-patterns:

1. **Hardcoded API Key** - API key is stored directly in code (`"sk-12345..."`)
2. **Hardcoded Port** - Port 8000 is fixed in code instead of environment variable
3. **Debug Mode Enabled** - `debug=True` in production is insecure
4. **No Health Check** - No `/health` or `/ready` endpoints for container orchestration
5. **No Graceful Shutdown** - No signal handlers for SIGTERM
6. **print() Logging** - Using `print()` instead of structured logging
7. **No Rate Limiting** - Anyone can call the API unlimited times
8. **In-Memory State** - Conversation history stored in local dict (not scalable)

### Exercise 1.3: Comparison Table

| Feature | Develop | Production | Why Important? |
|---------|---------|------------|----------------|
| Config | Hardcoded | Environment variables | Different environments have different values; secrets shouldn't be in code |
| Health Check | None | `/health` + `/ready` endpoints | Kubernetes/cloud platforms need to know if container is alive and ready |
| Logging | print() | JSON structured logs | Production logs need to be searchable, parseable by log aggregators |
| Shutdown | Abrupt | Graceful (SIGTERM handler) | Allows in-flight requests to complete before container stops |
| Rate Limiting | None | 20 req/min per user | Prevents abuse and protects resources |
| Authentication | None | API Key required | Public endpoints need authentication to prevent unauthorized access |
| State | In-memory | Redis | Stateless design allows horizontal scaling |

---

## Part 2: Docker

### Exercise 2.1: Dockerfile Questions

1. **Base image**: `python:3.11-slim` - Minimal Python image
2. **Working directory**: `/app`
3. **Why COPY requirements.txt first?**: Docker caches layers. If requirements.txt hasn't changed, it won't reinstall dependencies on code changes
4. **CMD vs ENTRYPOINT**:
   - `CMD`: Can be overridden by docker run arguments
   - `ENTRYPOINT`: More rigid, good for permanent command behavior

### Exercise 2.3: Image Size Comparison

- **Develop image**: ~1.2 GB (includes build tools, larger base)
- **Production image**: ~150 MB (slim base, multi-stage build)
- **Difference**: ~87% smaller

### Exercise 2.4: Docker Compose Architecture

```
┌─────────────────────────────────────┐
│         docker-compose.yml          │
├─────────────────────────────────────┤
│  nginx (port 80)                    │
│    └── proxy to agent:8000          │
│                                     │
│  agent (port 8000)                  │
│    └── FastAPI app                  │
│    └── depends on redis             │
│                                     │
│  redis (port 6379)                  │
│    └── data persistence             │
└─────────────────────────────────────┘
```

---

## Part 3: Cloud Deployment

### Exercise 3.1: Railway Deployment

*(To be filled after deployment)*

- **URL**: `https://your-app.railway.app`
- **Platform**: Railway
- **Test Result**: [Paste actual test output]

### Exercise 3.2: Render vs Railway Comparison

| Aspect | Railway | Render |
|--------|---------|--------|
| Config File | `railway.toml` | `render.yaml` |
| CLI | `@railway/cli` | Native |
| Free Tier | $5 credit | 750 hours/month |
| Setup | `railway init` + `railway up` | Connect GitHub + Blueprint |

---

## Part 4: API Security

### Exercise 4.1: API Key Authentication Test

```bash
# Without key - returns 401
$ curl http://localhost:8000/ask -X POST \
  -H "Content-Type: application/json" \
  -d '{"question": "Hello"}'
{"detail":"Invalid API key"}

# With correct key - returns 200
$ curl http://localhost:8000/ask -X POST \
  -H "X-API-Key: user1-secret-key" \
  -H "Content-Type: application/json" \
  -d '{"question": "Hello"}'
{"answer":"Hello! How can I help you today?","user_id":"user_001"}
```

### Exercise 4.2: JWT Authentication Flow

1. Client sends username/password to `/token`
2. Server validates and returns JWT token
3. Client uses `Authorization: Bearer <token>` for subsequent requests

### Exercise 4.3: Rate Limiting Test

```bash
# After 20 requests, returns 429
$ for i in {1..22}; do curl -s -H "X-API-Key: user1-secret-key" \
  http://localhost:8000/ask -X POST \
  -H "Content-Type: application/json" \
  -d '{"user_id":"test","question":"test '$i'"}'; done

# ... (rate limited after 20)
{"detail":"Rate limit exceeded. Max 20 requests per minute."}
```

### Exercise 4.4: Cost Guard Implementation

```python
def check_budget(user_id: str, estimated_cost: float = 0.01) -> bool:
    """
    - Track spending per user per month in Redis
    - Key format: budget:{user_id}:{YYYY-MM}
    - Reset monthly (32 day TTL for safety)
    - Returns False if exceeded $10/month limit
    """
    month_key = datetime.now().strftime("%Y-%m")
    key = f"budget:{user_id}:{month_key}"
    current = float(r.get(key) or 0)

    if current + estimated_cost > 10:
        return False

    r.incrbyfloat(key, estimated_cost)
    r.expire(key, 32 * 24 * 3600)
    return True
```

---

## Part 5: Scaling & Reliability

### Exercise 5.1: Health Check Implementation

- `/health` - Liveness probe: Returns 200 if process is running
- `/ready` - Readiness probe: Checks Redis connectivity, returns 503 if not ready

### Exercise 5.2: Graceful Shutdown

```python
import signal
import sys

def shutdown_handler(signum, frame):
    logger.info("Received SIGTERM, shutting down gracefully...")
    # Stop accepting new requests
    # Finish current requests
    # Close connections
    sys.exit(0)

signal.signal(signal.SIGTERM, shutdown_handler)
```

### Exercise 5.3: Stateless Design

**Anti-pattern (develop):**
```python
conversation_history = {}  # In-memory - not scalable!
```

**Correct (production):**
```python
# State in Redis
history = r.lrange(f"history:{user_id}", 0, -1)
```

### Exercise 5.4: Load Balancing with Nginx

```bash
docker compose up --scale agent=3
```

This starts 3 agent containers. Nginx distributes requests using `least_conn` algorithm.

### Exercise 5.5: Stateless Test Results

After killing one instance and making a request, the conversation history is preserved because it's stored in Redis (not in-memory).

---

## Part 6: Final Project Requirements Checklist

| Requirement | Status | Implementation |
|-------------|--------|----------------|
| Agent trả lời câu hỏi | ✅ | `/ask` endpoint |
| Conversation history | ✅ | Redis with 7-day TTL |
| Dockerized | ✅ | Multi-stage Dockerfile |
| Config từ env vars | ✅ | `pydantic-settings` |
| API key authentication | ✅ | `auth.py` |
| Rate limiting | ✅ | 20 req/min (sliding window) |
| Cost guard | ✅ | $10/month per user |
| Health check | ✅ | `/health` endpoint |
| Readiness check | ✅ | `/ready` endpoint |
| Graceful shutdown | ✅ | SIGTERM handler |
| Stateless design | ✅ | Redis storage |
| JSON logging | ✅ | Python logging |
| Deploy Railway/Render | ⏳ | Pending deployment |
