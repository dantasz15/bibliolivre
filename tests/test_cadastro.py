import unittest

from bibliolivre.errors import RegraNegocioError, ValidacaoError
from bibliolivre.services import normalizar_isbn
from tests.helpers import ISBN_A, ISBN_B, nova_biblioteca


class TestIsbn(unittest.TestCase):
    def test_aceita_com_e_sem_hifens(self):
        self.assertEqual(normalizar_isbn(ISBN_A), "9788535902778")
        self.assertEqual(normalizar_isbn("978 0306 406157"), ISBN_B)

    def test_rejeita_digito_verificador_errado(self):
        with self.assertRaises(ValidacaoError):
            normalizar_isbn("9780306406158")

    def test_rejeita_tamanho_ou_letras(self):
        for ruim in ["", "123", "97803064061X7", "97803064061570", None]:
            with self.subTest(ruim=ruim), self.assertRaises(ValidacaoError):
                normalizar_isbn(ruim)


class TestCadastro(unittest.TestCase):
    def setUp(self):
        self.bib, _ = nova_biblioteca()

    def test_cadastra_livro(self):
        livro = self.bib.cadastrar_livro(ISBN_A, " Dom Casmurro ", "Machado de Assis", 2)
        self.assertEqual(livro.titulo, "Dom Casmurro")
        self.assertEqual(self.bib.disponiveis(ISBN_A), 2)

    def test_livro_duplicado(self):
        self.bib.cadastrar_livro(ISBN_A, "X", "Y")
        with self.assertRaises(RegraNegocioError):
            self.bib.cadastrar_livro("9788535902778", "X", "Y")

    def test_exemplares_invalidos(self):
        for qtd in [0, -1, 1.5, True]:
            with self.subTest(qtd=qtd), self.assertRaises(ValidacaoError):
                self.bib.cadastrar_livro(ISBN_A, "X", "Y", qtd)

    def test_titulo_autor_vazios(self):
        with self.assertRaises(ValidacaoError):
            self.bib.cadastrar_livro(ISBN_A, "   ", "Y")
        with self.assertRaises(ValidacaoError):
            self.bib.cadastrar_livro(ISBN_A, "X", "")

    def test_cadastra_membro_normaliza_email(self):
        m = self.bib.cadastrar_membro("Ana", "  Ana@Email.COM ")
        self.assertEqual(m.email, "ana@email.com")

    def test_email_duplicado_case_insensitive(self):
        self.bib.cadastrar_membro("Ana", "ana@email.com")
        with self.assertRaises(RegraNegocioError):
            self.bib.cadastrar_membro("Outra Ana", "ANA@email.com")

    def test_nome_vazio(self):
        with self.assertRaises(ValidacaoError):
            self.bib.cadastrar_membro("   ", "ana@x.com")

    def test_email_invalido(self):
        for ruim in ["", "ana", "ana@", "ana@email", "a na@email.com"]:
            with self.subTest(ruim=ruim), self.assertRaises(ValidacaoError):
                self.bib.cadastrar_membro("Ana", ruim)

    def test_sql_injection_tratado_como_texto(self):
        titulo = "Livro'); DROP TABLE livros;--"
        self.bib.cadastrar_livro(ISBN_A, titulo, "Autor")
        self.assertEqual(self.bib.livros()[0].titulo, titulo)
