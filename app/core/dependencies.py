from fastapi import Depends, HTTPException
from sqlalchemy.orm import sessionmaker, Session
from jose import jwt, JWTError

from app.core.config import SECRET_KEY, ALGORITHM
from app.core.security import oauth2_schema
from app.database import db
from app.auth.models import Usuario


def pegar_sessao():
    try:
        SessionLocal = sessionmaker(bind=db)
        session = SessionLocal()
        yield session
    finally:
        session.close()


def verificar_token(
    token: str = Depends(oauth2_schema),
    session: Session = Depends(pegar_sessao)
):
    try:
        dic_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id_usuario = int(dic_info.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401, detail="Acesso Negado, verifique a validade do token")

    usuario = session.query(Usuario).filter(Usuario.id == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Acesso Inválido")

    return usuario