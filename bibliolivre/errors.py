class BiblioError(Exception):
    """Erro base do domínio."""


class ValidacaoError(BiblioError):
    """Dado de entrada inválido."""


class NaoEncontradoError(BiblioError):
    """Entidade inexistente."""


class RegraNegocioError(BiblioError):
    """Operação válida sintaticamente, mas proibida pelas regras (SPEC)."""
