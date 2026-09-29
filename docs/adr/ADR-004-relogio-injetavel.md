# ADR-004 — Relógio injetável para regras dependentes de data

**Status:** Aceita · **Data:** [PREENCHER]

## Contexto
Metade das regras (prazo, atraso, multa, renovação) depende da data atual. Testes que usam `date.today()` são não determinísticos e não conseguem simular "15 dias depois".

## Decisão
`Biblioteca(repo, hoje=callable)`. Em produção usa `date.today`; nos testes, um objeto `Relogio` que pode `avancar(dias)`.

## Alternativas
- **Monkeypatch/freezegun:** funciona, mas acopla os testes a detalhes internos (freezegun também é dependência externa).

## Consequências
+ Testes de borda exatos (dia do vencimento, dia seguinte, teto da multa).
− Um parâmetro a mais no construtor.
