from fastapi import FastAPI
from app.database import db
from app.routers.auth import router as auth_router

app = FastAPI(title="Finanças App")

app.include_router(auth_router)

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/health/db")
async def health_db():
    try:
        await db.command("ping")
        return {"status": "ok", "mongo": "conectado"}
    except Exception as e:
        return {"status": "erro", "detalhe": str(e)}
