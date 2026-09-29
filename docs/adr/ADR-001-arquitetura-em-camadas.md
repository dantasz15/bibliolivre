# ADR-001 — Arquitetura em camadas (CLI → Serviço → Repositório)

**Status:** Aceita · **Data:** [PREENCHER]

## Contexto
Equipe pequena, prazo curto, necessidade de testar regras de negócio isoladamente.

## Decisão
Três camadas: `cli` (entrada/saída), `services` (regras), `repository` (SQL). A camada de serviço não conhece argparse nem imprime nada; a CLI não contém regra de negócio.

## Alternativas consideradas
- **Script único:** mais rápido de escrever, mas impossível testar regras sem tocar no banco e no terminal.
- **Arquitetura hexagonal completa (ports/adapters, interfaces abstratas):** excesso de cerimônia para o tamanho do problema.

## Consequências
+ Regras testáveis com SQLite em memória; troca futura da interface (web) sem reescrever regras.
− Alguma duplicação de validação (ex.: ISBN normalizado no serviço e usado no repositório).
