# ADR-007 — Testes de propriedade sem dependências externas

**Status:** Aceita · **Data:** [PREENCHER]

## Contexto
Testes por exemplo só verificam os casos em que a equipe pensou. Os erros ERR-01 e RE-03 mostraram que as falhas estavam justamente nos casos não imaginados.

## Decisão
`tests/test_propriedades.py` executa milhares de operações aleatórias (emprestar, devolver, renovar, pagar, avançar dias) com **sementes fixas** e verifica após cada passo as invariantes da SPEC (disponibilidade entre 0 e o total, ≤ 3 ativos, sem título repetido, multa dentro do teto, nenhum empréstimo com multa pendente). Também verifica que a multa é monotônica em relação aos dias de atraso.

## Alternativas
- **Hypothesis:** mais poderosa (reduz o caso que falhou ao mínimo), mas viola RNF-01. Recomendada se o projeto aceitar dependências de desenvolvimento.

## Consequências
+ Cobre combinações que nenhum membro escreveria à mão; semente fixa torna falhas reproduzíveis.
− Não faz *shrinking*: uma falha precisa ser depurada a partir da sequência completa.
