# Política de Segurança

## Reportar vulnerabilidade
Não abra issue pública. Use **Security → Report a vulnerability** (aviso privado do GitHub) ou fale com um mantenedor listado no README. Resposta em até 7 dias.

## Medidas adotadas
| Risco | Mitigação | Evidência |
|---|---|---|
| Injeção de SQL | 100% das consultas parametrizadas (RNF-04) | `test_sql_injection_tratado_como_texto` + CodeQL |
| Condição de corrida (empréstimo duplo) | Transação `BEGIN IMMEDIATE` (ADR-006) | `test_ultimo_exemplar_disputado_por_varios_processos` |
| Vazamento de detalhes internos | CLI nunca exibe stack trace (RNF-06) | `test_banco_corrompido_nao_expoe_stack_trace` |
| Dados pessoais (LGPD) | Anonimização sob demanda (RF-09); `*.db` no `.gitignore` | `TestAnonimizacaoLGPD` |
| Dependências maliciosas | Zero dependências em produção (RNF-01) | `pyproject.toml` |
| Container | Imagem slim, usuário não-root | `Dockerfile` |
| Ações do CI desatualizadas | Dependabot semanal | `.github/dependabot.yml` |
| Análise estática | CodeQL a cada PR + semanal; Ruff | `.github/workflows/` |
