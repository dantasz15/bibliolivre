"""Interface de linha de comando (ADR-003)."""
import argparse
import os
import sqlite3
import sys
from typing import List, Optional

from .errors import BiblioError
from .repository import Repositorio
from .services import Biblioteca, formatar_reais


def _parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="bibliolivre", description="Empréstimos de biblioteca comunitária")
    p.add_argument("--db", default=os.environ.get("BIBLIO_DB", "bibliolivre.db"),
                   help="arquivo SQLite (padrão: $BIBLIO_DB ou bibliolivre.db)")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("livro-add", help="cadastra livro")
    s.add_argument("isbn")
    s.add_argument("titulo")
    s.add_argument("autor")
    s.add_argument("--exemplares", type=int, default=1)

    sub.add_parser("livros", help="lista acervo e disponibilidade")

    s = sub.add_parser("membro-add", help="cadastra membro")
    s.add_argument("nome")
    s.add_argument("email")

    s = sub.add_parser("emprestar", help="registra empréstimo")
    s.add_argument("isbn")
    s.add_argument("membro_id", type=int)

    s = sub.add_parser("devolver", help="registra devolução")
    s.add_argument("emprestimo_id", type=int)

    s = sub.add_parser("renovar", help="renova empréstimo")
    s.add_argument("emprestimo_id", type=int)

    sub.add_parser("atrasados", help="lista empréstimos atrasados")

    s = sub.add_parser("multa", help="consulta multa pendente")
    s.add_argument("membro_id", type=int)

    s = sub.add_parser("pagar", help="quita multas do membro")
    s.add_argument("membro_id", type=int)

    s = sub.add_parser("membro-anonimizar", help="LGPD: remove dados pessoais do membro")
    s.add_argument("membro_id", type=int)
    return p


def main(argv: Optional[List[str]] = None, bib: Optional[Biblioteca] = None) -> int:
    args = _parser().parse_args(argv)
    repo = None
    try:
        if bib is None:
            repo = Repositorio(args.db)  # ERR-07: abrir o banco também pode falhar
            bib = Biblioteca(repo)
        if args.cmd == "livro-add":
            livro = bib.cadastrar_livro(args.isbn, args.titulo, args.autor, args.exemplares)
            print(f"Livro cadastrado: {livro.titulo} ({livro.isbn}) x{livro.exemplares}")
        elif args.cmd == "livros":
            for livro in bib.livros():
                print(f"{livro.isbn} | {livro.titulo} | {livro.autor} | "
                      f"disponíveis: {bib.disponiveis(livro.isbn)}/{livro.exemplares}")
        elif args.cmd == "membro-add":
            m = bib.cadastrar_membro(args.nome, args.email)
            print(f"Membro #{m.id} cadastrado: {m.nome}")
        elif args.cmd == "emprestar":
            e = bib.emprestar(args.isbn, args.membro_id)
            print(f"Empréstimo #{e.id} registrado. Devolver até {e.data_prevista:%d/%m/%Y}")
        elif args.cmd == "devolver":
            e = bib.devolver(args.emprestimo_id)
            extra = f" Multa: {formatar_reais(e.multa_centavos)}" if e.multa_centavos else ""
            print(f"Empréstimo #{e.id} devolvido.{extra}")
        elif args.cmd == "renovar":
            e = bib.renovar(args.emprestimo_id)
            print(f"Empréstimo #{e.id} renovado até {e.data_prevista:%d/%m/%Y}")
        elif args.cmd == "atrasados":
            itens = bib.atrasados()
            if not itens:
                print("Nenhum empréstimo em atraso.")
            for e in itens:
                print(f"#{e.id} | livro {e.isbn} | membro {e.membro_id} | venceu {e.data_prevista:%d/%m/%Y}")
        elif args.cmd == "multa":
            print(f"Multa pendente: {formatar_reais(bib.multa_pendente(args.membro_id))}")
        elif args.cmd == "pagar":
            print(f"Pago: {formatar_reais(bib.pagar_multas(args.membro_id))}")
        elif args.cmd == "membro-anonimizar":
            m = bib.anonimizar_membro(args.membro_id)
            print(f"Dados pessoais removidos: {m.nome}")
        return 0
    except BiblioError as exc:
        print(f"Erro: {exc}", file=sys.stderr)
        return 1
    except sqlite3.Error:
        # RNF-06: nunca expor stack trace ou SQL ao usuário
        print("Erro: falha ao acessar o banco de dados", file=sys.stderr)
        return 3
    finally:
        if repo is not None:
            repo.fechar()
