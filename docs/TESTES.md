# Resultados dos Testes e Cobertura

## Execução local da candidata à release

Em 24 de outubro de 2026, foram executados os testes na branch de preparação `release/1.0.0`, em Python 3.12.3 e coverage.py 7.17.0:

```text
Ran 47 tests in 1.135s
OK

Name                        Stmts   Miss  Cover
bibliolivre/__init__.py         1      0   100%
bibliolivre/cli.py             83      0   100%
bibliolivre/errors.py           4      0   100%
bibliolivre/models.py          27      0   100%
bibliolivre/repository.py      90      0   100%
bibliolivre/services.py       143      0   100%
TOTAL                         348      0   100%
```

- [Log textual completo da execução local](evidencias/coverage-20261024T172458Z.txt)
- [Relatório de cobertura XML](evidencias/coverage-20261024T172458Z.xml)
- O log registra o SHA base `369bbf1` e indica que a árvore continha alterações não commitadas durante essa medição. Ele é evidência local da candidata; o workflow do PR deve validar o commit versionado.

O lint Ruff (`ruff check bibliolivre tests`) passou e `make demo` executou o fluxo de cadastro, empréstimo, renovação, devolução e anonimização. Docker não estava instalado no ambiente local; por isso, nenhum resultado Docker local é declarado.

## CI e validação da release

O workflow [`.github/workflows/ci.yml`](../.github/workflows/ci.yml) está configurado para executar lint, testes/cobertura em Python 3.10, 3.11 e 3.12, além do harness e build Docker. [`.github/workflows/codeql.yml`](../.github/workflows/codeql.yml) configura análise CodeQL.

## Execução oficial do PR

No commit `0eb22aa` (`0eb22aa289c33546ccd4f6aa2abd2b9892dd75cd`), o evento `pull_request` concluiu com sucesso:

- [PR #9 — `release/1.0.0` → `main`](https://github.com/dantasz15/bibliolivre/pull/9).
- [CI do PR — execução 40212336837](https://github.com/dantasz15/bibliolivre/actions/runs/40212336837): lint, matriz Python 3.10–3.12 e Docker passaram.
- [CodeQL — execução 40212336839](https://github.com/dantasz15/bibliolivre/actions/runs/40212336839): análise concluída com sucesso.
- A página do PR reportou 12 checks bem-sucedidos, 0 falhas e 0 pendências. Em cada versão Python, 47 testes passaram e 348/348 instruções tiveram cobertura (100%). O harness Docker também executou 47 testes e a imagem runtime foi construída.
- Artefatos `coverage-python-3.10`, `coverage-python-3.11` e `coverage-python-3.12` foram enviados ao Actions e ficam disponíveis até 24/11/2026. Para baixar: `gh run download 40212336837 --repo dantasz15/bibliolivre`.

A primeira execução da candidata identificou em Python 3.10 a ausência do suporte TOML do Coverage. A dependência foi corrigida para `coverage[toml]`; os resultados acima pertencem ao commit corrigido. O PR continua draft e a integração/release ainda depende de aprovação humana independente.

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

`make coverage` executa a suíte e falha se a cobertura de linhas ficar abaixo de 95%. Os relatórios XML/textuais são criados em `docs/evidencias/`; o workflow também publica artefatos temporários por execução.

## Organização da suíte e rastreabilidade

| Arquivo | Foco |
|---|---|
| `tests/test_cadastro.py` | ISBN-13, cadastro de livro/membro, validações e unicidade. |
| `tests/test_emprestimos.py` | Prazos, limites, devolução, renovação e multas. |
| `tests/test_cli.py` | Contrato de saída da CLI, persistência e tratamento de erros. |
| `tests/test_lgpd_concorrencia.py` | Anonimização, colisão de e-mail sentinela, rollback e oito conexões disputando um exemplar. |
| `tests/test_propriedades.py` | Simulações determinísticas de invariantes e monotonicidade do cálculo da multa. |

A cobertura de linhas mede execução de código, não prova que os requisitos estejam completos nem que não existam defeitos.
