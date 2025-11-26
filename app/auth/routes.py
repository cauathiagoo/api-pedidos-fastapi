from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone
from jose import jwt

from app.auth.models import Usuario
from app.core.security import bcrypt_context
from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from app.auth.schemas import UsuarioSchema, LoginSchema
from app.core.dependencies import pegar_sessao, verificar_token

router = APIRouter(prefix="/auth", tags=["auth"])


def criar_token(id_usuario, duracao_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    data_expiracao = datetime.now(timezone.utc) + duracao_token
    dic_info = {"sub": str(id_usuario), "exp": data_expiracao}
    jwt_codificado = jwt.encode(dic_info, SECRET_KEY, ALGORITHM)
    return jwt_codificado


def autenticar_usuario(email, senha, session):
    usuario = session.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        return False
    elif not bcrypt_context.verify(senha, usuario.senha):
        return False
    return usuario


@router.get("/")
async def home():
    return {"mensagem": "Você acessou a rota padrão de autenticação", "autenticado": False}


@router.post("/criar_conta")
async def criar_conta(usuario_schema: UsuarioSchema, session: Session = Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.email == usuario_schema.email).first()
    if usuario:
        raise HTTPException(status_code=400, detail="E-mail do usuário já cadastrado")

    senha_criptografada = bcrypt_context.hash(usuario_schema.senha)
    novo_usuario = Usuario(
        usuario_schema.nome,
        usuario_schema.email,
        senha_criptografada,
        usuario_schema.ativo,
        usuario_schema.admin,
    )
    session.add(novo_usuario)
    session.commit()
    return {"mensagem": f"usuário cadastrado com sucesso: {usuario_schema.email}"}


@router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou credenciais inválidas")

    access_token = criar_token(usuario.id)
    refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7))
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer",
    }


@router.get("/refresh")
async def use_refresh_token(usuario: Usuario = Depends(verificar_token)):
    access_token = criar_token(usuario.id)
    return {
        "access_token": access_token,
        "token_type": "Bearer",
    }


@router.post("/login-form")
async def login_form(dados_formulario: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(dados_formulario.username, dados_formulario.password, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou credenciais inválidas")

    access_token = criar_token(usuario.id)
    return {
        "access_token": access_token,
        "token_type": "Bearer",
    }


@router.delete("/deletar_usuario/{id_usuario}", summary="Deletar um usuário pelo ID")
async def deletar_usuario(
    id_usuario: int,
    session: Session = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token)
):
    # Somente admin pode deletar 
    if not usuario.admin:
        raise HTTPException(status_code=401, detail="Você não tem autorização para deletar usuários")

    usuario_deletar = session.query(Usuario).filter(Usuario.id == id_usuario).first()

    if not usuario_deletar:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    session.delete(usuario_deletar)
    session.commit()

    return {"mensagem": f"O usuário: {usuario_deletar.email} foi deletado com sucesso!"}


@router.get("/listar_usuarios", summary="Listar todos os usuários (somente admin)")
async def listar_usuarios(
    session: Session = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token)
):
    # Verificar se a rota é admin
    if not usuario.admin:
        raise HTTPException(status_code=401, detail="Você não tem autorização para fazer essa operação")

    usuarios = session.query(Usuario).all()

    # Formatar para não mostrar senha
    lista_formatada = [
        {
            "id": u.id,
            "nome": u.nome,
            "email": u.email,
            "ativo": u.ativo,
            "admin": u.admin
        }
        for u in usuarios
    ]

    return {"usuarios": lista_formatada}