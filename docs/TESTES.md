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

## Validação oficial da release no GitHub Actions

A matriz final do PR #9 foi executada em 26 de outubro de 2026 no head `e9771d6` e terminou com 12 verificações aprovadas, sem falhas ou pendências. Depois da integração, CI e CodeQL foram executados novamente no commit `6df47b8453967c3326b9dba40e780477a8452077` de `main`; ambos concluíram com sucesso.

- [PR #9 — `release/1.0.0` → `main`, integrado](https://github.com/dantasz15/bibliolivre/pull/9).
- [CI pós-merge — execução 40414632362](https://github.com/dantasz15/bibliolivre/actions/runs/40414632362): execução no commit integrado `6df47b8`, concluída com sucesso.
- [CodeQL pós-merge — execução 40414632359](https://github.com/dantasz15/bibliolivre/actions/runs/40414632359): análise no commit integrado, concluída com sucesso.
- [CI do PR — execução 40413951139](https://github.com/dantasz15/bibliolivre/actions/runs/40413951139) e [CodeQL do PR — execução 40413951136](https://github.com/dantasz15/bibliolivre/actions/runs/40413951136): lint, testes Python 3.10–3.12, harness/build Docker e análise de segurança aprovados no head `e9771d6`.
- Em cada versão Python, 47 testes passaram e 348/348 instruções tiveram cobertura de linhas (100%). O harness Docker executou os mesmos 47 testes e construiu a imagem runtime.
- Os artefatos `coverage-python-3.10`, `coverage-python-3.11` e `coverage-python-3.12` foram publicados pelo workflow do PR e permanecem sujeitos ao prazo de retenção do GitHub Actions.
- [Release oficial `v1.0.0`](https://github.com/dantasz15/bibliolivre/releases/tag/v1.0.0), publicada a partir de `main` no commit de merge.

A primeira execução da matriz encontrou suporte TOML ausente do Coverage em Python 3.10. A dependência de desenvolvimento foi corrigida para `coverage[toml]`; os números acima pertencem às execuções posteriores aprovadas. A cobertura mede linhas executadas e não prova ausência de defeitos.

**Governança:** o PR #9 foi revisado pelo autor por se tratar de trabalho individual. Não houve aprovação independente registrada; por autorização expressa, a regra de proteção exige PR, mas o número de aprovações obrigatórias está configurado como zero. Os checks aprovados são evidência automatizada, não revisão por pares.

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
