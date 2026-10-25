# Política de Segurança

## Reportar vulnerabilidade

Não publique detalhes de uma vulnerabilidade em issue pública. Use **Security → Report a vulnerability** caso o recurso de reporte privado esteja habilitado no GitHub; se não estiver disponível, contate o mantenedor por [@dantasz15](https://github.com/dantasz15). Não há prazo de resposta de segurança formalmente estabelecido.

## Controles e evidências

| Risco | Controle implementado | Evidência/limite |
|---|---|---|
| Injeção de SQL | Consultas de dados usam parâmetros SQLite. | `test_sql_injection_tratado_como_texto`; CodeQL configurado, resultado depende de execução remota. |
| Empréstimos concorrentes | `BEGIN IMMEDIATE` engloba validação e gravação. | Teste com oito conexões independentes no mesmo arquivo local; não valida NAS/SMB/NFS. |
| Exposição de detalhes internos | CLI captura erros SQLite e não apresenta stack trace. | `test_banco_corrompido_nao_expoe_stack_trace`. |
| Dados pessoais | Anonimização substitui nome e e-mail; arquivos `.db` são ignorados no Git e Docker. | `TestAnonimizacaoLGPD`; a função não comprova conformidade legal integral. |
| Dependências | Nenhuma dependência de runtime; ferramentas dev são opcionais. | `pyproject.toml`. |
| Container | Usuário não-root, `.dockerignore` e volume nomeado. | `Dockerfile`, `.dockerignore`, `docker-compose.yml`; execução Docker remota ainda deve ser confirmada. |
| Atualizações de workflows | Dependabot configurado para dependências/actions. | `.github/dependabot.yml`; dependabot não substitui revisão nem análise de alertas. |
| Análise estática | Workflow CodeQL e Ruff configurados. | `.github/workflows/codeql.yml`, `.github/workflows/ci.yml`; configuração não equivale a resultado verde. |

## Escopo

BiblioLivre é uma aplicação CLI local, sem autenticação de usuários, servidor web ou sincronização em rede. Não use o projeto como serviço multiusuário em rede sem avaliação adicional de segurança, privacidade, backup e disponibilidade.
