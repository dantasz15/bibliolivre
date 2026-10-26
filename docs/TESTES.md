# Resultados dos Testes e Cobertura

## Execução local histórica

Em 24 de outubro de 2026, a suíte foi executada na branch de preparação `release/1.0.0`, com Python 3.12.3 e coverage.py 7.17.0. O log local registra 47 testes aprovados e 100% de cobertura de linhas em 348 instruções. Essa execução é histórica: o próprio log registra que a árvore de trabalho tinha alterações não commitadas. Ela não deve ser usada isoladamente como prova de uma release integrada.

- [Log textual da execução local](evidencias/coverage-20261024T172458Z.txt)
- [Relatório XML local](evidencias/coverage-20261024T172458Z.xml)

O lint Ruff passou e `make demo` executou o fluxo de cadastro, empréstimo, renovação, devolução e anonimização. O ambiente local não tinha Docker; a evidência Docker abaixo vem do GitHub Actions.

## Reexecução local — 26 de outubro de 2026

Após atualizar a documentação, a suíte foi executada novamente localmente na branch `release/1.0.0`, no commit de referência `c099ba1`. As únicas alterações presentes na árvore eram documentais. Python 3.12.3 executou 47 testes sem falhas e mediu 100% de cobertura de linhas em 348 instruções; Ruff, `make demo` e `pip check` também passaram. A demonstração usou dados fictícios e o banco temporário foi removido ao final.

- [Log completo local](evidencias/coverage-20261026T222747Z.txt)
- [Relatório XML local](evidencias/coverage-20261026T222747Z.xml)

## Validação oficial da candidata no GitHub Actions

A validação remota mais recente observada para a candidata foi executada no head `c099ba18d7fb7ba1f9bb555cfe773a7ddb338d81` do PR #9. Em 25 de outubro de 2026, o evento `pull_request` terminou com sucesso:

- [PR #9 — `release/1.0.0` → `main`](https://github.com/dantasz15/bibliolivre/pull/9).
- [CI do PR — execução 40213447824](https://github.com/dantasz15/bibliolivre/actions/runs/40213447824): lint, testes Python 3.10–3.12 e harness/build Docker aprovados.
- [CodeQL v4 — execução 40213447836](https://github.com/dantasz15/bibliolivre/actions/runs/40213447836): análise concluída com sucesso.
- O PR reportou 12 verificações bem-sucedidas, nenhuma falha e nenhuma pendência. Em cada versão Python, 47 testes passaram e 348/348 instruções tiveram cobertura de linhas (100%). O harness Docker executou os mesmos 47 testes e construiu a imagem runtime.
- Os artefatos `coverage-python-3.10`, `coverage-python-3.11` e `coverage-python-3.12` foram publicados pelo workflow; consulte a execução de CI para baixá-los enquanto estiverem retidos.

A primeira execução da matriz encontrou suporte TOML ausente do Coverage em Python 3.10. A dependência de desenvolvimento foi corrigida para `coverage[toml]`; os números acima pertencem à execução posterior aprovada.

**Limite importante:** o PR #9 continua aberto, sem aprovação independente e sem merge. Portanto, esses dados validam a candidata no PR; ainda não são evidência de uma tag ou release integrada em `main`. A cobertura mede linhas executadas e não prova ausência de defeitos.

## Comandos reproduzíveis

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
make lint
make coverage

docker compose run --build --rm test
docker build --target runtime -t bibliolivre:1.0.0 .
```

`make coverage` falha se a cobertura de linhas ficar abaixo de 95%. Os relatórios textuais/XML são gerados em `docs/evidencias/`; o workflow também publica artefatos temporários por execução.

## Organização da suíte e rastreabilidade

| Arquivo | Foco |
|---|---|
| `tests/test_cadastro.py` | ISBN-13, cadastro de livro/membro, validações e unicidade. |
| `tests/test_emprestimos.py` | Prazos, limites, devolução, renovação e multas. |
| `tests/test_cli.py` | Contrato de saída da CLI, persistência e tratamento de erros. |
| `tests/test_lgpd_concorrencia.py` | Anonimização, colisão de e-mail sentinela, rollback e oito conexões disputando um exemplar. |
| `tests/test_propriedades.py` | Simulações determinísticas de invariantes e monotonicidade do cálculo da multa. |

A suíte combina testes de domínio e de integração local. Não há uma validação end-to-end de interface web: o escopo entregue é uma CLI offline para SQLite local.
