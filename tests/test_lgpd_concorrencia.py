import os
import tempfile
import threading
import unittest

from bibliolivre.errors import NaoEncontradoError, RegraNegocioError
from bibliolivre.repository import Repositorio
from bibliolivre.services import PRAZO_DIAS, Biblioteca
from tests.helpers import ISBN_A, Relogio, nova_biblioteca


class TestAnonimizacaoLGPD(unittest.TestCase):
    """RF-09: direito de eliminação de dados pessoais (LGPD art. 18, VI)."""

    def setUp(self):
        self.bib, self.relogio = nova_biblioteca()
        self.bib.cadastrar_livro(ISBN_A, "Livro", "Autor")
        self.ana = self.bib.cadastrar_membro("Ana Souza", "ana@x.com")

    def test_remove_nome_e_email_preservando_historico(self):
        e = self.bib.emprestar(ISBN_A, self.ana.id)
        self.bib.devolver(e.id)
        m = self.bib.anonimizar_membro(self.ana.id)
        self.assertNotIn("Ana", m.nome)
        self.assertNotIn("ana@x.com", m.email)
        self.assertIsNotNone(self.bib.repo.buscar_emprestimo(e.id))  # estatística preservada

    def test_email_original_fica_livre_para_novo_cadastro(self):
        self.bib.anonimizar_membro(self.ana.id)
        self.bib.cadastrar_membro("Ana Souza", "ana@x.com")

    def test_bloqueia_com_emprestimo_ativo(self):
        self.bib.emprestar(ISBN_A, self.ana.id)
        with self.assertRaisesRegex(RegraNegocioError, "ativos"):
            self.bib.anonimizar_membro(self.ana.id)

    def test_bloqueia_com_multa_pendente(self):
        e = self.bib.emprestar(ISBN_A, self.ana.id)
        self.relogio.avancar(PRAZO_DIAS + 3)
        self.bib.devolver(e.id)
        with self.assertRaisesRegex(RegraNegocioError, "multa"):
            self.bib.anonimizar_membro(self.ana.id)

    def test_membro_inexistente(self):
        with self.assertRaises(NaoEncontradoError):
            self.bib.anonimizar_membro(999)


class TestTransacoes(unittest.TestCase):
    """RNF-07 / ADR-006: operações atômicas."""

    def test_rollback_quando_regra_falha_no_meio(self):
        bib, _ = nova_biblioteca()
        bib.cadastrar_livro(ISBN_A, "Livro", "Autor")
        with self.assertRaises(NaoEncontradoError):
            bib.emprestar(ISBN_A, 999)
        # a conexão continua utilizável e sem transação pendente
        self.assertFalse(bib.repo.conn.in_transaction)
        self.assertEqual(bib.disponiveis(ISBN_A), 1)

    def test_ultimo_exemplar_disputado_por_varios_processos(self):
        """ERR-06: 8 conexões independentes disputam 1 exemplar -> só 1 vence."""
        with tempfile.TemporaryDirectory() as tmp:
            caminho = os.path.join(tmp, "concorrencia.db")
            base = Biblioteca(Repositorio(caminho), hoje=Relogio())
            base.cadastrar_livro(ISBN_A, "Livro", "Autor", 1)
            ids = [base.cadastrar_membro(f"M{i}", f"m{i}@x.com").id for i in range(8)]
            base.repo.fechar()

            barreira = threading.Barrier(len(ids))
            sucessos, recusas, outros = [], [], []

            def tentar(membro_id):
                bib = Biblioteca(Repositorio(caminho), hoje=Relogio())
                try:
                    barreira.wait()
                    bib.emprestar(ISBN_A, membro_id)
                    sucessos.append(membro_id)
                except RegraNegocioError:
                    recusas.append(membro_id)
                except Exception as exc:  # noqa: BLE001 - registrar qualquer falha inesperada
                    outros.append(exc)
                finally:
                    bib.repo.fechar()

            threads = [threading.Thread(target=tentar, args=(i,)) for i in ids]
            for t in threads:
                t.start()
            for t in threads:
                t.join()

            self.assertEqual(outros, [])
            self.assertEqual(len(sucessos), 1)
            self.assertEqual(len(recusas), len(ids) - 1)
