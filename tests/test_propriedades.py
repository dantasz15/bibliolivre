"""Testes de propriedade (invariantes) com simulação aleatória reprodutível.

Em vez de verificar um caso específico, executa milhares de operações aleatórias
ao longo de dias simulados e confere, após cada passo, que as invariantes da
SPEC continuam verdadeiras. A semente é fixa para que uma falha seja reproduzível.
"""
import random
import unittest
from datetime import date, timedelta

from bibliolivre.errors import BiblioError
from bibliolivre.services import (MAX_EMPRESTIMOS, MAX_RENOVACOES,
                                  TETO_MULTA_CENTAVOS, Biblioteca)
from tests.helpers import nova_biblioteca

ISBNS = ["9788535902778", "9780306406157", "9788533302273", "9780140449136", "9780262033848"]


class TestInvariantes(unittest.TestCase):
    def verificar_invariantes(self, bib):
        for livro in bib.livros():
            disp = bib.disponiveis(livro.isbn)
            self.assertGreaterEqual(disp, 0, "RN-08: disponibilidade negativa")
            self.assertLessEqual(disp, livro.exemplares)
        ativos_por_membro = {}
        for e in bib.repo.todos_ativos():
            ativos_por_membro.setdefault(e.membro_id, []).append(e.isbn)
            self.assertLessEqual(e.renovacoes, MAX_RENOVACOES, "RN-05")
        for isbns in ativos_por_membro.values():
            self.assertLessEqual(len(isbns), MAX_EMPRESTIMOS, "RN-02")
            self.assertEqual(len(isbns), len(set(isbns)), "RN-04")

    def test_simulacao_aleatoria(self):
        for semente in range(5):
            with self.subTest(semente=semente):
                self._simular(random.Random(semente), passos=400)

    def _simular(self, rnd, passos):
        bib, relogio = nova_biblioteca()
        for isbn in ISBNS:
            bib.cadastrar_livro(isbn, f"Livro {isbn}", "Autor", rnd.randint(1, 3))
        membros = [bib.cadastrar_membro(f"M{i}", f"m{i}@x.com").id for i in range(6)]

        for _ in range(passos):
            acao = rnd.choice(["emprestar", "emprestar", "devolver", "renovar", "pagar", "dia"])
            ativos = bib.repo.todos_ativos()
            try:
                if acao == "emprestar":
                    membro = rnd.choice(membros)
                    tinha_multa = bib.multa_pendente(membro) > 0
                    bib.emprestar(rnd.choice(ISBNS), membro)
                    self.assertFalse(tinha_multa, "RN-03: emprestou com multa pendente")
                elif acao == "devolver" and ativos:
                    e = bib.devolver(rnd.choice(ativos).id)
                    self.assertTrue(0 <= e.multa_centavos <= TETO_MULTA_CENTAVOS, "RN-07")
                elif acao == "renovar" and ativos:
                    bib.renovar(rnd.choice(ativos).id)
                elif acao == "pagar":
                    bib.pagar_multas(rnd.choice(membros))
                else:
                    relogio.avancar(rnd.randint(1, 10))
            except BiblioError:
                pass  # recusas são esperadas; o que importa são as invariantes
            self.verificar_invariantes(bib)

    def test_multa_monotona_e_limitada(self):
        """RN-06/07: mais dias de atraso nunca geram multa menor, e nunca passa do teto."""
        prazo = date(2026, 1, 1)
        anterior = 0
        for dias in range(-30, 400):
            atual = Biblioteca.calcular_multa(prazo, prazo + timedelta(days=dias))
            self.assertGreaterEqual(atual, anterior)
            self.assertLessEqual(atual, TETO_MULTA_CENTAVOS)
            anterior = atual
