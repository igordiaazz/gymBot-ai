import enum
from sqlalchemy import Column, Integer, String, Boolean, Enum
from database import Base


class NivelExperiencia(enum.Enum):
    iniciante = "iniciante"
    intermediario = "intermediario"
    avancado = "avancado"

class Aluno(Base):
    __tablename__ = "alunos"

    id = Column(Integer, primary_key=True, index=True)
    telefone = Column(String, unique=True, index=True)
    nome = Column(String)
    objetivo = Column(String)
    nivel_experiencia = Column(Enum(NivelExperiencia), default=NivelExperiencia.intermediario)
    mensalidade_ativa = Column(Boolean, default=True)