# ADR-003 — Interface de linha de comando com argparse

**Status:** Aceita · **Data:** [PREENCHER]

## Contexto
Precisávamos de uma interface utilizável e testável dentro do prazo, sem dependências.

## Decisão
CLI com subcomandos (`argparse`). A função `main(argv, bib)` recebe argumentos e retorna o código de saída, o que permite testes de integração sem subprocessos.

## Alternativas
- **Web (Flask/FastAPI):** melhor usabilidade, mas adiciona dependências, servidor e superfície de ataque. Mantida no backlog.
- **Click/Typer:** API mais agradável, mas viola RNF-01.

## Consequências
+ Portátil, scriptável, fácil de testar.
− Menos amigável para voluntários leigos → mitigado com mensagens claras e exemplos no README.
