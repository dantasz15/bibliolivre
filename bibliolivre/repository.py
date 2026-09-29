"""Persistência em SQLite (ADR-002). Somente consultas parametrizadas."""
import sqlite3
from contextlib import contextmanager
from datetime import date
from typing import Iterator, List, Optional

from .models import Emprestimo, Livro, Membro

SCHEMA = """
CREATE TABLE IF NOT EXISTS livros (
    isbn TEXT PRIMARY KEY,
    titulo TEXT NOT NULL,
    autor TEXT NOT NULL,
    exemplares INTEGER NOT NULL CHECK (exemplares >= 1)
);
CREATE TABLE IF NOT EXISTS membros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS emprestimos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    isbn TEXT NOT NULL REFERENCES livros(isbn),
    membro_id INTEGER NOT NULL REFERENCES membros(id),
    data_emprestimo TEXT NOT NULL,
    data_prevista TEXT NOT NULL,
    data_devolucao TEXT,
    renovacoes INTEGER NOT NULL DEFAULT 0,
    multa_centavos INTEGER NOT NULL DEFAULT 0,
    multa_paga INTEGER NOT NULL DEFAULT 0
);
"""


def _d(valor: Optional[str]) -> Optional[date]:
    return date.fromisoformat(valor) if valor else None


class Repositorio:
    def __init__(self, caminho: str = ":memory:"):
        # isolation_level=None: transações controladas explicitamente (ADR-006)
        self.conn = sqlite3.connect(caminho, timeout=10, isolation_level=None,
                                    check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")
        self._em_transacao = False
        with self.transacao():
            for comando in filter(None, (c.strip() for c in SCHEMA.split(";"))):
                self.conn.execute(comando)

    @contextmanager
    def transacao(self) -> Iterator[None]:
        """BEGIN IMMEDIATE: reserva o lock de escrita já na leitura, evitando
        que dois processos emprestem o último exemplar ao mesmo tempo (ERR-06)."""
        if self._em_transacao:
            yield
            return
        self.conn.execute("BEGIN IMMEDIATE")
        self._em_transacao = True
        try:
            yield
            self.conn.execute("COMMIT")
        except BaseException:
            self.conn.execute("ROLLBACK")
            raise
        finally:
            self._em_transacao = False

    def fechar(self) -> None:
        self.conn.close()

    # ---------- livros ----------
    def inserir_livro(self, livro: Livro) -> None:
        with self.transacao():
            self.conn.execute(
                "INSERT INTO livros (isbn, titulo, autor, exemplares) VALUES (?, ?, ?, ?)",
                (livro.isbn, livro.titulo, livro.autor, livro.exemplares),
            )

    def buscar_livro(self, isbn: str) -> Optional[Livro]:
        r = self.conn.execute("SELECT * FROM livros WHERE isbn = ?", (isbn,)).fetchone()
        return Livro(r["isbn"], r["titulo"], r["autor"], r["exemplares"]) if r else None

    def listar_livros(self) -> List[Livro]:
        rows = self.conn.execute("SELECT * FROM livros ORDER BY titulo").fetchall()
        return [Livro(r["isbn"], r["titulo"], r["autor"], r["exemplares"]) for r in rows]

    # ---------- membros ----------
    def inserir_membro(self, nome: str, email: str) -> Membro:
        with self.transacao():
            cur = self.conn.execute(
                "INSERT INTO membros (nome, email) VALUES (?, ?)", (nome, email)
            )
        return Membro(cur.lastrowid, nome, email)

    def buscar_membro(self, membro_id: int) -> Optional[Membro]:
        r = self.conn.execute("SELECT * FROM membros WHERE id = ?", (membro_id,)).fetchone()
        return Membro(r["id"], r["nome"], r["email"]) if r else None

    def buscar_membro_por_email(self, email: str) -> Optional[Membro]:
        r = self.conn.execute("SELECT * FROM membros WHERE email = ?", (email,)).fetchone()
        return Membro(r["id"], r["nome"], r["email"]) if r else None

    # ---------- empréstimos ----------
    def _emp(self, r) -> Emprestimo:
        return Emprestimo(
            id=r["id"], isbn=r["isbn"], membro_id=r["membro_id"],
            data_emprestimo=_d(r["data_emprestimo"]), data_prevista=_d(r["data_prevista"]),
            data_devolucao=_d(r["data_devolucao"]), renovacoes=r["renovacoes"],
            multa_centavos=r["multa_centavos"], multa_paga=bool(r["multa_paga"]),
        )

    def inserir_emprestimo(self, isbn: str, membro_id: int, inicio: date, prevista: date) -> Emprestimo:
        with self.transacao():
            cur = self.conn.execute(
                "INSERT INTO emprestimos (isbn, membro_id, data_emprestimo, data_prevista) "
                "VALUES (?, ?, ?, ?)",
                (isbn, membro_id, inicio.isoformat(), prevista.isoformat()),
            )
        return self.buscar_emprestimo(cur.lastrowid)

    def buscar_emprestimo(self, emp_id: int) -> Optional[Emprestimo]:
        r = self.conn.execute("SELECT * FROM emprestimos WHERE id = ?", (emp_id,)).fetchone()
        return self._emp(r) if r else None

    def ativos_do_membro(self, membro_id: int) -> List[Emprestimo]:
        rows = self.conn.execute(
            "SELECT * FROM emprestimos WHERE membro_id = ? AND data_devolucao IS NULL",
            (membro_id,),
        ).fetchall()
        return [self._emp(r) for r in rows]

    def ativos_do_livro(self, isbn: str) -> int:
        return self.conn.execute(
            "SELECT COUNT(*) FROM emprestimos WHERE isbn = ? AND data_devolucao IS NULL",
            (isbn,),
        ).fetchone()[0]

    def todos_ativos(self) -> List[Emprestimo]:
        rows = self.conn.execute(
            "SELECT * FROM emprestimos WHERE data_devolucao IS NULL ORDER BY data_prevista"
        ).fetchall()
        return [self._emp(r) for r in rows]

    def registrar_devolucao(self, emp_id: int, quando: date, multa_centavos: int) -> None:
        with self.transacao():
            self.conn.execute(
                "UPDATE emprestimos SET data_devolucao = ?, multa_centavos = ?, multa_paga = ? "
                "WHERE id = ?",
                (quando.isoformat(), multa_centavos, 1 if multa_centavos == 0 else 0, emp_id),
            )

    def registrar_renovacao(self, emp_id: int, nova_prevista: date) -> None:
        with self.transacao():
            self.conn.execute(
                "UPDATE emprestimos SET data_prevista = ?, renovacoes = renovacoes + 1 WHERE id = ?",
                (nova_prevista.isoformat(), emp_id),
            )

    def multa_pendente(self, membro_id: int) -> int:
        return self.conn.execute(
            "SELECT COALESCE(SUM(multa_centavos), 0) FROM emprestimos "
            "WHERE membro_id = ? AND multa_paga = 0",
            (membro_id,),
        ).fetchone()[0]

    def anonimizar_membro(self, membro_id: int) -> None:
        with self.transacao():
            self.conn.execute(
                "UPDATE membros SET nome = ?, email = ? WHERE id = ?",
                (f"Membro anonimizado #{membro_id}", f"anonimizado-{membro_id}@invalido.local", membro_id),
            )

    def quitar_multas(self, membro_id: int) -> int:
        valor = self.multa_pendente(membro_id)
        with self.transacao():
            self.conn.execute(
                "UPDATE emprestimos SET multa_paga = 1 WHERE membro_id = ? AND data_devolucao IS NOT NULL",
                (membro_id,),
            )
        return valor
