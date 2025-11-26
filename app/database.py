from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

# Conexão do banco
db = create_engine("sqlite:///banco.db")

# Base de modelos
Base = declarative_base()
