import io
import os
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout

from bibliolivre.cli import main
from tests.helpers import ISBN_A, nova_biblioteca


def rodar(db, *args):
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = main(["--db", db, *args])
    return code, out.getvalue(), err.getvalue()


class TestCli(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db = os.path.join(self.tmp.name, "t.db")

    def tearDown(self):
        self.tmp.cleanup()

    def test_fluxo_ponta_a_ponta_persistente(self):
        self.assertEqual(rodar(self.db, "livro-add", ISBN_A, "Dom Casmurro", "Machado")[0], 0)
        self.assertEqual(rodar(self.db, "membro-add", "Ana", "ana@x.com")[0], 0)
        code, out, _ = rodar(self.db, "emprestar", ISBN_A, "1")
        self.assertEqual(code, 0)
        self.assertIn("Empréstimo #1", out)
        _, out, _ = rodar(self.db, "livros")
        self.assertIn("disponíveis: 0/1", out)
        self.assertIn("devolvido", rodar(self.db, "devolver", "1")[1])
        self.assertIn("R$ 0,00", rodar(self.db, "multa", "1")[1])

    def test_anonimizar_pela_cli(self):
        rodar(self.db, "membro-add", "Ana", "ana@x.com")
        code, out, _ = rodar(self.db, "membro-anonimizar", "1")
        self.assertEqual(code, 0)
        self.assertIn("anonimizado", out)

    def test_banco_corrompido_nao_expoe_stack_trace(self):
        with open(self.db, "w") as f:
            f.write("isto não é um banco sqlite")
        code, out, err = rodar(self.db, "livros")
        self.assertEqual(code, 3)
        self.assertIn("falha ao acessar o banco", err)
        self.assertNotIn("Traceback", err)

    def test_atrasados_vazio(self):
        self.assertIn("Nenhum", rodar(self.db, "atrasados")[1])

    def test_erro_retorna_codigo_1_e_mensagem(self):
        code, _, err = rodar(self.db, "emprestar", ISBN_A, "1")
        self.assertEqual(code, 1)
        self.assertIn("Erro:", err)


class TestCliComRelogio(unittest.TestCase):
    """CLI com biblioteca injetada: permite simular a passagem do tempo."""

    def cmd(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = main(list(args), bib=self.bib)
        return code, out.getvalue(), err.getvalue()

    def setUp(self):
        self.bib, self.relogio = nova_biblioteca()
        self.cmd("livro-add", ISBN_A, "Dom Casmurro", "Machado")
        self.cmd("membro-add", "Ana", "ana@x.com")
        self.cmd("emprestar", ISBN_A, "1")

    def test_renovar(self):
        self.assertIn("renovado até 23/03/2026", self.cmd("renovar", "1")[1])

    def test_atrasados_multa_e_pagamento(self):
        self.relogio.avancar(17)
        self.assertIn("venceu 16/03/2026", self.cmd("atrasados")[1])
        self.assertIn("Multa: R$ 1,50", self.cmd("devolver", "1")[1])
        self.assertIn("R$ 1,50", self.cmd("multa", "1")[1])
        self.assertIn("Pago: R$ 1,50", self.cmd("pagar", "1")[1])
