# ADR-005 — Valores monetários em centavos inteiros

**Status:** Aceita (substitui a abordagem inicial com `float`) · **Data:** [PREENCHER]

## Contexto
A primeira versão calculava multa como `dias * 0.5` em `float`. Somas de várias multas geravam valores como `1.4999999` e comparações `== 1.5` falhavam (ver ERR-02).

## Decisão
Toda quantia é `int` em centavos; conversão para "R$ x,yy" só na exibição (`formatar_reais`).

## Alternativas
- **`decimal.Decimal`:** correto, mas mais verboso e exige cuidado ao persistir no SQLite.

## Consequências
+ Aritmética exata e simples; persistência como INTEGER.
− Nomes de campos precisam deixar claro a unidade (`multa_centavos`).
