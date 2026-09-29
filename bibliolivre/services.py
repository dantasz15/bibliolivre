"""Regras de negócio. Cada regra referencia o requisito da SPEC (docs/SPEC.md)."""
import re
from datetime import date, timedelta
from typing import Callable, List

from .errors import NaoEncontradoError, RegraNegocioError, ValidacaoError
from .models import Emprestimo, Livro, Membro
from .repository import Repositorio

PRAZO_DIAS = 14               # RN-01
MAX_EMPRESTIMOS = 3           # RN-02
MAX_RENOVACOES = 1            # RN-05
RENOVACAO_DIAS = 7            # RN-05
MULTA_DIA_CENTAVOS = 50       # RN-06
TETO_MULTA_CENTAVOS = 2000    # RN-07 (adicionada na re-especificação RE-02)

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def normalizar_isbn(isbn: str) -> str:
    """RF-01: aceita ISBN-13 com ou sem hífens/espaços e valida o dígito verificador."""
    limpo = re.sub(r"[-\s]", "", isbn or "")
    if not re.fullmatch(r"\d{13}", limpo):
        raise ValidacaoError("ISBN deve ter 13 dígitos numéricos")
    soma = sum(int(d) * (1 if i % 2 == 0 else 3) for i, d in enumerate(limpo[:12]))
    if (10 - soma % 10) % 10 != int(limpo[12]):
        raise ValidacaoError("ISBN com dígito verificador inválido")
    return limpo


def formatar_reais(centavos: int) -> str:
    return f"R$ {centavos // 100},{centavos % 100:02d}"


class Biblioteca:
    def __init__(self, repo: Repositorio, hoje: Callable[[], date] = date.today):
        self.repo = repo
        self.hoje = hoje  # relógio injetável (ADR-004) para testes determinísticos

    # ---------------- cadastro ----------------
    def cadastrar_livro(self, isbn: str, titulo: str, autor: str, exemplares: int = 1) -> Livro:
        with self.repo.transacao():
            return self._cadastrar_livro(isbn, titulo, autor, exemplares)

    def _cadastrar_livro(self, isbn: str, titulo: str, autor: str, exemplares: int) -> Livro:
        isbn = normalizar_isbn(isbn)
        titulo, autor = (titulo or "").strip(), (autor or "").strip()
        if not titulo or not autor:
            raise ValidacaoError("Título e autor são obrigatórios")
        if isinstance(exemplares, bool) or not isinstance(exemplares, int) or exemplares < 1:
            raise ValidacaoError("Quantidade de exemplares deve ser inteiro >= 1")
        if self.repo.buscar_livro(isbn):
            raise RegraNegocioError(f"Livro {isbn} já cadastrado")
        livro = Livro(isbn, titulo, autor, exemplares)
        self.repo.inserir_livro(livro)
        return livro

    def cadastrar_membro(self, nome: str, email: str) -> Membro:
        with self.repo.transacao():
            return self._cadastrar_membro(nome, email)

    def _cadastrar_membro(self, nome: str, email: str) -> Membro:
        nome = (nome or "").strip()
        email = (email or "").strip().lower()
        if not nome:
            raise ValidacaoError("Nome é obrigatório")
        if not EMAIL_RE.match(email):
            raise ValidacaoError("E-mail inválido")
        if self.repo.buscar_membro_por_email(email):
            raise RegraNegocioError("E-mail já cadastrado")
        return self.repo.inserir_membro(nome, email)

    # ---------------- consultas ----------------
    def _livro(self, isbn: str) -> Livro:
        livro = self.repo.buscar_livro(normalizar_isbn(isbn))
        if not livro:
            raise NaoEncontradoError("Livro não encontrado")
        return livro

    def _membro(self, membro_id: int) -> Membro:
        membro = self.repo.buscar_membro(membro_id)
        if not membro:
            raise NaoEncontradoError("Membro não encontrado")
        return membro

    def _emprestimo(self, emp_id: int) -> Emprestimo:
        emp = self.repo.buscar_emprestimo(emp_id)
        if not emp:
            raise NaoEncontradoError("Empréstimo não encontrado")
        return emp

    def disponiveis(self, isbn: str) -> int:
        livro = self._livro(isbn)
        return livro.exemplares - self.repo.ativos_do_livro(livro.isbn)

    def livros(self) -> List[Livro]:
        return self.repo.listar_livros()

    def atrasados(self) -> List[Emprestimo]:
        hoje = self.hoje()
        return [e for e in self.repo.todos_ativos() if e.data_prevista < hoje]

    def multa_pendente(self, membro_id: int) -> int:
        self._membro(membro_id)
        return self.repo.multa_pendente(membro_id)

    # ---------------- operações ----------------
    def emprestar(self, isbn: str, membro_id: int) -> Emprestimo:
        with self.repo.transacao():  # RNF-07: verificação + gravação atômicas
            return self._emprestar(isbn, membro_id)

    def _emprestar(self, isbn: str, membro_id: int) -> Emprestimo:
        livro = self._livro(isbn)
        self._membro(membro_id)
        hoje = self.hoje()

        if self.repo.multa_pendente(membro_id) > 0:                          # RN-03
            raise RegraNegocioError("Membro possui multa pendente")
        ativos = self.repo.ativos_do_membro(membro_id)
        if any(e.data_prevista < hoje for e in ativos):                      # RN-03 (RE-03)
            raise RegraNegocioError("Membro possui empréstimo em atraso")
        if len(ativos) >= MAX_EMPRESTIMOS:                                   # RN-02
            raise RegraNegocioError(f"Limite de {MAX_EMPRESTIMOS} empréstimos atingido")
        if any(e.isbn == livro.isbn for e in ativos):                        # RN-04
            raise RegraNegocioError("Membro já está com um exemplar deste livro")
        if self.disponiveis(livro.isbn) <= 0:                                # RN-08
            raise RegraNegocioError("Nenhum exemplar disponível")

        return self.repo.inserir_emprestimo(
            livro.isbn, membro_id, hoje, hoje + timedelta(days=PRAZO_DIAS)   # RN-01
        )

    @staticmethod
    def calcular_multa(prevista: date, devolucao: date) -> int:
        """RN-06/RN-07: devolver NO dia previsto não gera multa (corrige ERR-01)."""
        dias_atraso = max(0, (devolucao - prevista).days)
        return min(dias_atraso * MULTA_DIA_CENTAVOS, TETO_MULTA_CENTAVOS)

    def devolver(self, emp_id: int) -> Emprestimo:
        with self.repo.transacao():
            return self._devolver(emp_id)

    def _devolver(self, emp_id: int) -> Emprestimo:
        emp = self._emprestimo(emp_id)
        if not emp.ativo:
            raise RegraNegocioError("Empréstimo já devolvido")               # ERR-03
        hoje = self.hoje()
        if hoje < emp.data_emprestimo:
            raise ValidacaoError("Data de devolução anterior ao empréstimo")
        self.repo.registrar_devolucao(emp.id, hoje, self.calcular_multa(emp.data_prevista, hoje))
        return self.repo.buscar_emprestimo(emp.id)

    def renovar(self, emp_id: int) -> Emprestimo:
        with self.repo.transacao():
            return self._renovar(emp_id)

    def _renovar(self, emp_id: int) -> Emprestimo:
        emp = self._emprestimo(emp_id)
        if not emp.ativo:
            raise RegraNegocioError("Empréstimo já devolvido")
        if emp.renovacoes >= MAX_RENOVACOES:                                 # RN-05
            raise RegraNegocioError("Limite de renovações atingido")
        if self.hoje() > emp.data_prevista:                                  # RN-05 (RE-01)
            raise RegraNegocioError("Empréstimo em atraso não pode ser renovado")
        nova = emp.data_prevista + timedelta(days=RENOVACAO_DIAS)
        self.repo.registrar_renovacao(emp.id, nova)
        return self.repo.buscar_emprestimo(emp.id)

    def pagar_multas(self, membro_id: int) -> int:
        with self.repo.transacao():
            self._membro(membro_id)
            return self.repo.quitar_multas(membro_id)

    def anonimizar_membro(self, membro_id: int) -> Membro:
        """RF-09 (LGPD, art. 18): elimina nome e e-mail, preservando o histórico
        de empréstimos para estatística. Só é permitido sem pendências."""
        with self.repo.transacao():
            self._membro(membro_id)
            if self.repo.ativos_do_membro(membro_id):
                raise RegraNegocioError("Membro possui empréstimos ativos")
            if self.repo.multa_pendente(membro_id) > 0:
                raise RegraNegocioError("Membro possui multa pendente")
            self.repo.anonimizar_membro(membro_id)
            return self.repo.buscar_membro(membro_id)
