from fastapi import APIRouter, Depends, HTTPException
from app.models import BudgetCreate
from app.database import db
from app.auth import verificar_token
from bson import ObjectId

router = APIRouter(prefix="/budgets", tags=["Orçamentos"])

def formatar(b):
    b["id"] = str(b["_id"])
    del b["_id"]
    return b

@router.post("/")
async def criar_orcamento(dados: BudgetCreate, usuario=Depends(verificar_token)):
    orcamento = dados.dict()
    orcamento["usuario_id"] = usuario["id"]
    resultado = await db.budgets.insert_one(orcamento)
    return {"id": str(resultado.inserted_id), "mensagem": "Orçamento criado!"}

@router.get("/")
async def listar_orcamentos(usuario=Depends(verificar_token)):
    orcamentos = []
    async for b in db.budgets.find({"usuario_id": usuario["id"]}):
        orcamentos.append(formatar(b))
    return orcamentos

@router.put("/{id}")
async def editar_orcamento(id: str, dados: BudgetCreate, usuario=Depends(verificar_token)):
    resultado = await db.budgets.update_one(
        {"_id": ObjectId(id), "usuario_id": usuario["id"]},
        {"$set": dados.dict()}
    )
    if resultado.matched_count == 0:
        raise HTTPException(status_code=404, detail="Orçamento não encontrado")
    return {"mensagem": "Orçamento atualizado!"}

@router.delete("/{id}")
async def deletar_orcamento(id: str, usuario=Depends(verificar_token)):
    resultado = await db.budgets.delete_one(
        {"_id": ObjectId(id), "usuario_id": usuario["id"]}
    )
    if resultado.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Orçamento não encontrado")
    return {"mensagem": "Orçamento deletado!"}

@router.get("/status")
async def status_orcamentos(usuario=Depends(verificar_token)):
    orcamentos = []
    async for b in db.budgets.find({"usuario_id": usuario["id"]}):
        orcamentos.append(b)

    resultado = []
    for b in orcamentos:
        total_gasto = 0.0
        async for t in db.transactions.find({
            "usuario_id": usuario["id"],
            "categoria": b["categoria"],
            "tipo": "gasto"
        }):
            data = t.get("data")
            if data and data.month == b["mes"] and data.year == b["ano"]:
                total_gasto += t.get("valor", 0.0)

        limite = b["limite_mensal"]
        disponivel = limite - total_gasto
        percentual = (total_gasto / limite * 100) if limite > 0 else 0
        alerta = percentual >= 80

        resultado.append({
            "categoria": b["categoria"],
            "mes": b["mes"],
            "ano": b["ano"],
            "limite": limite,
            "gasto": round(total_gasto, 2),
            "disponivel": round(disponivel, 2),
            "percentual": round(percentual, 1),
            "alerta": alerta
        })

    return resultado