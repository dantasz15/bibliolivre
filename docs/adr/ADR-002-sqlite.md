# ADR-002 — SQLite como armazenamento

**Status:** Aceita · **Data:** [PREENCHER]

## Contexto
RNF-01/RNF-02: sem internet, sem servidor, computadores modestos, voluntários sem conhecimento de infraestrutura.

## Decisão
SQLite via módulo `sqlite3` da biblioteca padrão, com `PRAGMA foreign_keys = ON` e consultas 100% parametrizadas.

## Alternativas
- **PostgreSQL/MySQL:** robustos, mas exigem servidor e instalação — inviável para o público-alvo.
- **JSON/CSV:** simples, porém sem integridade referencial nem transações; risco de corromper dados em escrita concorrente.

## Consequências
+ Zero instalação; backup = copiar um arquivo; testes usam `:memory:`.
− Não indicado para muitos usuários simultâneos em rede (fora do escopo).
