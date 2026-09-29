from datetime import date, timedelta

from bibliolivre.repository import Repositorio
from bibliolivre.services import Biblioteca

ISBN_A = "978-85-359-0277-8"   # válido
ISBN_B = "9780306406157"       # válido
ISBN_C = "9788533302273"       # válido


class Relogio:
    """Relógio controlável para testes determinísticos (ADR-004)."""

    def __init__(self, inicio=date(2026, 3, 2)):
        self.atual = inicio

    def __call__(self):
        return self.atual

    def avancar(self, dias):
        self.atual += timedelta(days=dias)


def nova_biblioteca():
    relogio = Relogio()
    bib = Biblioteca(Repositorio(":memory:"), hoje=relogio)
    return bib, relogio
