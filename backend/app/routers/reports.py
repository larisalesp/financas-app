from fastapi import APIRouter, Depends
from app.database import db
from app.auth import verificar_token
from typing import Optional

router = APIRouter(prefix="/reports", tags=["Relatórios"])

@router.get("/summary")
async def resumo_mensal(
    mes: Optional[int] = None,
    ano: Optional[int] = None,
    usuario=Depends(verificar_token)
):
    filtro = {"usuario_id": usuario["id"]}

    receitas = 0.0
    gastos = 0.0

    async for t in db.transactions.find(filtro):
        data = t.get("data")
        if mes and data and data.month != mes:
            continue
        if ano and data and data.year != ano:
            continue
        if t.get("tipo") == "receita":
            receitas += t.get("valor", 0.0)
        elif t.get("tipo") == "gasto":
            gastos += t.get("valor", 0.0)

    return {
        "mes": mes,
        "ano": ano,
        "receitas": round(receitas, 2),
        "gastos": round(gastos, 2),
        "saldo": round(receitas - gastos, 2)
    }

@router.get("/by-category")
async def resumo_por_categoria(
    mes: Optional[int] = None,
    ano: Optional[int] = None,
    usuario=Depends(verificar_token)
):
    filtro = {"usuario_id": usuario["id"], "tipo": "gasto"}
    categorias = {}

    async for t in db.transactions.find(filtro):
        data = t.get("data")
        if mes and data and data.month != mes:
            continue
        if ano and data and data.year != ano:
            continue
        cat = t.get("categoria", "Sem categoria")
        categorias[cat] = categorias.get(cat, 0.0) + t.get("valor", 0.0)

    resultado = [
        {"categoria": cat, "total": round(valor, 2)}
        for cat, valor in sorted(categorias.items(), key=lambda x: x[1], reverse=True)
    ]
    return resultado

@router.get("/by-month")
async def resumo_por_mes(
    ano: Optional[int] = None,
    usuario=Depends(verificar_token)
):
    filtro = {"usuario_id": usuario["id"]}
    meses = {}

    async for t in db.transactions.find(filtro):
        data = t.get("data")
        if not data:
            continue
        if ano and data.year != ano:
            continue

        chave = f"{data.year}-{str(data.month).zfill(2)}"
        if chave not in meses:
            meses[chave] = {"receitas": 0.0, "gastos": 0.0}

        if t.get("tipo") == "receita":
            meses[chave]["receitas"] += t.get("valor", 0.0)
        elif t.get("tipo") == "gasto":
            meses[chave]["gastos"] += t.get("valor", 0.0)

    resultado = [
        {
            "periodo": chave,
            "receitas": round(v["receitas"], 2),
            "gastos": round(v["gastos"], 2),
            "saldo": round(v["receitas"] - v["gastos"], 2)
        }
        for chave, v in sorted(meses.items())
    ]
    return resultado