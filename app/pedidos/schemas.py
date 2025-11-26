from pydantic import BaseModel


class PedidoSchema(BaseModel):
    id_usuario: int

    class Config:
        from_attributes = True


class ItemPedidoSchema(BaseModel):
    quantidade: int
    sabor: str
    tamanho: str
    preco_unitario: float

    class Config:
        from_attributes = True