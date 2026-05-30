# SKILL: FastAPI AI API

> Async Python API with AI integration, auth, rate limiting.

## Project Structure
```
ai-api/
├── app/
│   ├── main.py, config.py, database.py
│   ├── routers/auth.py, ai.py, users.py
│   ├── services/ai_service.py, auth_service.py
│   └── dependencies/auth.py
├── requirements.txt
└── Dockerfile
```

## Core Setup
```python
# main.py
from fastapi import FastAPI
from app.routers import auth, ai, users

app = FastAPI()
app.include_router(auth.router, prefix="/api/auth")
app.include_router(ai.router, prefix="/api/ai")
app.include_router(users.router, prefix="/api/users")

@app.get("/health")
async def health():
    return {"status": "ok"}
```

## AI Service (OpenRouter)
```python
import httpx

class AIService:
    async def chat(self, messages: list, model: str = None):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {API_KEY}"},
                json={"model": model or "openrouter/owl-alpha", "messages": messages},
                timeout=60,
            )
            return response.json()["choices"][0]["message"]["content"]

ai = AIService()

@router.post("/ai/chat")
async def chat(req: ChatRequest, user=Depends(get_current_user)):
    response = await ai.chat(req.messages, req.model)
    return {"response": response}
```

## Auth
```python
from jose import jwt
from passlib.context import CryptContext
pwd = CryptContext(schemes=["bcrypt"])

# Login -> return JWT
token = jwt.encode({"sub": user.id, "exp": ...}, SECRET_KEY, "HS256")

# Dependency
async def get_current_user(token = Depends(HTTPBearer())):
    payload = jwt.decode(token.credentials, SECRET_KEY, ["HS256"])
    return await get_user(payload["sub"])

# Role check
def require_role(*roles):
    async def checker(user = Depends(get_current_user)):
        if user.role not in roles:
            raise HTTPException(403, "Forbidden")
        return user
    return checker
```

## Requirements
```txt
fastapi==0.111.* uvicorn[standard]==0.30.* sqlalchemy==2.0.*
asyncpg==0.29.* pydantic-settings==2.3.* python-jose==3.3.*
passlib[bcrypt]==1.7.* httpx==0.27.*
```

## Deploy (Railway)
```bash
# Procfile: web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
railway up
```
