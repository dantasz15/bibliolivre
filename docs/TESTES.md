# Resultados dos Testes Automatizados

## Como executar
```bash
python -m unittest discover -s tests -t . -v
```
Também executado no CI (`.github/workflows/ci.yml`) em Python 3.10, 3.11 e 3.12 a cada push/PR, após o lint, e novamente dentro do container Docker. **Nenhum PR pode ser mergeado com o CI vermelho** (regra de proteção da branch `main`).

## Resultado da execução final
```
Ran 46 tests in 0.35s

OK

Cobertura de linhas do pacote bibliolivre: 100% (mínimo exigido no CI: 95%)
```
> Anexar aqui o print/link da última execução verde do GitHub Actions: [PREENCHER]

## Organização do test harness
| Arquivo | Tipo | Foco |
|---|---|---|
| `tests/helpers.py` | apoio | `Relogio` falso, biblioteca com SQLite em memória, ISBNs válidos |
| `tests/test_cadastro.py` | unidade | RF-01, RF-02, validações e injeção de SQL |
| `tests/test_emprestimos.py` | unidade | RF-03 a RF-06, RN-01 a RN-08 |
| `tests/test_cli.py` | integração | fluxo ponta a ponta com arquivo SQLite real, códigos de saída, banco corrompido, CLI com relógio simulado |
| `tests/test_lgpd_concorrencia.py` | integração | RF-09 (LGPD), rollback, 8 conexões disputando o último exemplar |
| `tests/test_propriedades.py` | propriedade | 5 simulações × 400 operações aleatórias verificando invariantes; monotonicidade da multa |

## Pirâmide de testes
| Nível | Qtde | O que garante |
|---|---|---|
| Unidade | 30 | Cada regra RN/RF isoladamente |
| Integração | 11 | CLI + banco real + concorrência |
| Propriedade | 2 (2.000+ operações) | Invariantes sob combinações imprevistas |
| Estática | CI | Ruff (estilo/erros) + CodeQL (segurança) |

## Matriz de rastreabilidade (SPEC → testes)
| Regra | Cenário normal | Cenários de borda |
|---|---|---|
| RF-01 ISBN | `test_aceita_com_e_sem_hifens` | dígito errado, vazio, `None`, letras, 14 dígitos |
| RF-01 livro | `test_cadastra_livro` | duplicado com formatação diferente, exemplares 0/−1/1.5/`True`, título em branco |
| RF-02 | `test_cadastra_membro_normaliza_email` | e-mail duplicado com maiúsculas, 5 formatos inválidos |
| RN-01 | `test_fluxo_normal` | — |
| RN-02 | `test_limite_de_tres` | 4º empréstimo bloqueado |
| RN-03 | `test_bloqueio_por_multa_e_desbloqueio_apos_pagar` | `test_bloqueio_por_atraso_ativo` |
| RN-04 | `test_mesmo_livro_duas_vezes` | com 2 exemplares disponíveis |
| RN-05 | `test_renova_uma_vez` | último dia permitido, atrasado, já devolvido, 2ª renovação |
| RN-06/07 | `test_calculo_multa_limites` | −3, 0, 1, 10, 40 (teto exato), 41, 365 dias |
| RN-08 | `test_sem_exemplar_disponivel` | — |
| RF-04 | `test_devolucao_libera_exemplar` | devolução duplicada, ID inexistente, no dia do prazo |
| RF-06 | `test_atrasados` | um vencido e outro não |
| RNF-04 | `test_sql_injection_tratado_como_texto` | — |
| RNF-06 | `test_erro_retorna_codigo_1_e_mensagem` | `test_banco_corrompido_nao_expoe_stack_trace` |
| RF-09 | `test_remove_nome_e_email_preservando_historico` | empréstimo ativo, multa pendente, inexistente, reuso do e-mail |
| RNF-07 | `test_rollback_quando_regra_falha_no_meio` | `test_ultimo_exemplar_disputado_por_varios_processos` |
| Invariantes | `test_simulacao_aleatoria` | `test_multa_monotona_e_limitada` (−30 a 400 dias) |
