from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass(frozen=True)
class Livro:
    isbn: str
    titulo: str
    autor: str
    exemplares: int


@dataclass(frozen=True)
class Membro:
    id: int
    nome: str
    email: str


@dataclass(frozen=True)
class Emprestimo:
    id: int
    isbn: str
    membro_id: int
    data_emprestimo: date
    data_prevista: date
    data_devolucao: Optional[date]
    renovacoes: int
    multa_centavos: int
    multa_paga: bool

    @property
    def ativo(self) -> bool:
        return self.data_devolucao is None
