from fastapi import APIRouter, HTTPException, status
from app.database import db
from app.models import UserCreate
from app.auth import hash_senha, verificar_senha, criar_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate):
    existe = await db["usuarios"].find_one({"email": user.email})
    if existe:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    
    novo_usuario = {
        "nome": user.nome,
        "email": user.email,
        "senha": hash_senha(user.senha)
    }
    await db["usuarios"].insert_one(novo_usuario)
    return {"mensagem": "Usuário criado com sucesso"}

@router.post("/login")
async def login(user: UserCreate):
    usuario = await db["usuarios"].find_one({"email": user.email})
    if not usuario or not verificar_senha(user.senha, usuario["senha"]):
        raise HTTPException(status_code=401, detail="Email ou senha incorretos")
    
    token = criar_token({"sub": usuario["email"]})
    return {"access_token": token, "token_type": "bearer"}
