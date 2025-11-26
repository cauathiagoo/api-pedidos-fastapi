from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import pegar_sessao, verificar_token
from app.schemas import PedidoSchema, ItemPedidoSchema
from app.pedidos.models import Pedido, ItemPedido
from app.auth.models import Usuario


router = APIRouter(
    prefix="/pedidos",
    tags=["pedidos"],
    dependencies=[Depends(verificar_token)]
)

# ROTA PADRÃO
@router.get("/")
async def pedidos_home():
    return {"mensagem": "Rota de pedidos. Autenticação obrigatória."}

# CRIAR PEDIDO (POST)
@router.post("/", summary="Criar novo pedido")
async def criar_pedido(
    pedido_schema: PedidoSchema,
    session: Session = Depends(pegar_sessao)
):
    novo_pedido = Pedido(usuario=pedido_schema.id_usuario)
    session.add(novo_pedido)
    session.commit()
    return {"mensagem": "Pedido criado com sucesso", "id": novo_pedido.id}


# CANCELAR PEDIDO (PUT)
@router.put("/{id_pedido}/cancelar", summary="Cancelar pedido pelo ID")
async def cancelar_pedido(
    id_pedido: int,
    session: Session = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token)
):

    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()

    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Acesso negado")

    pedido.status = "CANCELADO"
    session.commit()

    return {
        "mensagem": "Pedido cancelado com sucesso",
        "pedido": pedido
    }

# LISTAR PEDIDOS (GET)
@router.get("/listar", summary="Listar todos os pedidos (somente admin)")
async def listar_pedidos(
    session: Session = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token)
):
    if not usuario.admin:
        raise HTTPException(status_code=401, detail="Acesso negado")

    pedidos = session.query(Pedido).all()
    return {"pedidos": pedidos}


# REMOVER ITEM DO PEDIDO
@router.delete("/item/{id_item_pedido}", summary="Remover item de um pedido")
async def remover_item_pedido(
    id_item_pedido: int,
    session: Session = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token)
):
    item_pedido = session.query(ItemPedido).filter(ItemPedido.id == id_item_pedido).first()

    if not item_pedido:
        raise HTTPException(status_code=404, detail="Item não encontrado")

    pedido = session.query(Pedido).filter(Pedido.id == item_pedido.pedido).first()

    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Acesso negado")

    session.delete(item_pedido)

    pedido.calcular_preco()
    session.commit()

    return {
        "mensagem": "Item removido com sucesso",
        "pedido": pedido,
        "quantidade_itens": len(pedido.itens)
    }
