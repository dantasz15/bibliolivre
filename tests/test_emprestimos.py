import unittest
from datetime import timedelta

from bibliolivre.errors import NaoEncontradoError, RegraNegocioError, ValidacaoError
from bibliolivre.services import Biblioteca, PRAZO_DIAS
from tests.helpers import ISBN_A, ISBN_B, ISBN_C, nova_biblioteca

ISBN_D = "9780140449136"


class BaseEmprestimo(unittest.TestCase):
    def setUp(self):
        self.bib, self.relogio = nova_biblioteca()
        for isbn in (ISBN_A, ISBN_B, ISBN_C, ISBN_D):
            self.bib.cadastrar_livro(isbn, f"Livro {isbn}", "Autor", 1)
        self.ana = self.bib.cadastrar_membro("Ana", "ana@x.com")
        self.beto = self.bib.cadastrar_membro("Beto", "beto@x.com")


class TestEmprestar(BaseEmprestimo):
    def test_fluxo_normal(self):
        e = self.bib.emprestar(ISBN_A, self.ana.id)
        self.assertEqual(e.data_prevista, self.relogio() + timedelta(days=PRAZO_DIAS))
        self.assertEqual(self.bib.disponiveis(ISBN_A), 0)

    def test_sem_exemplar_disponivel(self):
        self.bib.emprestar(ISBN_A, self.ana.id)
        with self.assertRaises(RegraNegocioError):
            self.bib.emprestar(ISBN_A, self.beto.id)

    def test_limite_de_tres(self):
        for isbn in (ISBN_A, ISBN_B, ISBN_C):
            self.bib.emprestar(isbn, self.ana.id)
        with self.assertRaisesRegex(RegraNegocioError, "Limite"):
            self.bib.emprestar(ISBN_D, self.ana.id)

    def test_mesmo_livro_duas_vezes(self):
        self.bib.repo.conn.execute("UPDATE livros SET exemplares = 2 WHERE isbn = ?", (ISBN_A,))
        self.bib.emprestar(ISBN_A, self.ana.id)
        with self.assertRaisesRegex(RegraNegocioError, "já está"):
            self.bib.emprestar(ISBN_A, self.ana.id)

    def test_membro_ou_livro_inexistente(self):
        with self.assertRaises(NaoEncontradoError):
            self.bib.emprestar(ISBN_A, 999)
        with self.assertRaises(NaoEncontradoError):
            self.bib.emprestar("9781234567897", self.ana.id)

    def test_bloqueio_por_atraso_ativo(self):
        self.bib.emprestar(ISBN_A, self.ana.id)
        self.relogio.avancar(PRAZO_DIAS + 1)
        with self.assertRaisesRegex(RegraNegocioError, "atraso"):
            self.bib.emprestar(ISBN_B, self.ana.id)

    def test_bloqueio_por_multa_e_desbloqueio_apos_pagar(self):
        e = self.bib.emprestar(ISBN_A, self.ana.id)
        self.relogio.avancar(PRAZO_DIAS + 2)
        self.bib.devolver(e.id)
        with self.assertRaisesRegex(RegraNegocioError, "multa"):
            self.bib.emprestar(ISBN_B, self.ana.id)
        self.assertEqual(self.bib.pagar_multas(self.ana.id), 100)
        self.assertEqual(self.bib.multa_pendente(self.ana.id), 0)
        self.bib.emprestar(ISBN_B, self.ana.id)


class TestDevolucaoEMulta(BaseEmprestimo):
    def test_calculo_multa_limites(self):
        p = self.relogio()
        casos = {-3: 0, 0: 0, 1: 50, 10: 500, 40: 2000, 41: 2000, 365: 2000}
        for dias, esperado in casos.items():
            with self.subTest(dias=dias):
                self.assertEqual(Biblioteca.calcular_multa(p, p + timedelta(days=dias)), esperado)

    def test_devolucao_no_dia_do_prazo_sem_multa(self):
        e = self.bib.emprestar(ISBN_A, self.ana.id)
        self.relogio.avancar(PRAZO_DIAS)
        self.assertEqual(self.bib.devolver(e.id).multa_centavos, 0)

    def test_devolucao_libera_exemplar(self):
        e = self.bib.emprestar(ISBN_A, self.ana.id)
        self.bib.devolver(e.id)
        self.assertEqual(self.bib.disponiveis(ISBN_A), 1)

    def test_devolucao_duplicada(self):
        e = self.bib.emprestar(ISBN_A, self.ana.id)
        self.bib.devolver(e.id)
        with self.assertRaises(RegraNegocioError):
            self.bib.devolver(e.id)

    def test_relogio_anterior_ao_emprestimo(self):
        """Proteção contra relógio do computador desajustado."""
        e = self.bib.emprestar(ISBN_A, self.ana.id)
        self.relogio.avancar(-1)
        with self.assertRaises(ValidacaoError):
            self.bib.devolver(e.id)

    def test_devolucao_inexistente(self):
        with self.assertRaises(NaoEncontradoError):
            self.bib.devolver(42)

    def test_atrasados(self):
        e1 = self.bib.emprestar(ISBN_A, self.ana.id)
        self.relogio.avancar(5)
        self.bib.emprestar(ISBN_B, self.beto.id)
        self.relogio.avancar(PRAZO_DIAS - 4)  # só o 1º venceu
        self.assertEqual([x.id for x in self.bib.atrasados()], [e1.id])


class TestRenovacao(BaseEmprestimo):
    def test_renova_uma_vez(self):
        e = self.bib.emprestar(ISBN_A, self.ana.id)
        r = self.bib.renovar(e.id)
        self.assertEqual(r.data_prevista, e.data_prevista + timedelta(days=7))
        with self.assertRaisesRegex(RegraNegocioError, "renovações"):
            self.bib.renovar(e.id)

    def test_renovar_no_ultimo_dia_permitido(self):
        e = self.bib.emprestar(ISBN_A, self.ana.id)
        self.relogio.avancar(PRAZO_DIAS)
        self.bib.renovar(e.id)

    def test_nao_renova_atrasado(self):
        e = self.bib.emprestar(ISBN_A, self.ana.id)
        self.relogio.avancar(PRAZO_DIAS + 1)
        with self.assertRaisesRegex(RegraNegocioError, "atraso"):
            self.bib.renovar(e.id)

    def test_nao_renova_devolvido(self):
        e = self.bib.emprestar(ISBN_A, self.ana.id)
        self.bib.devolver(e.id)
        with self.assertRaises(RegraNegocioError):
            self.bib.renovar(e.id)
