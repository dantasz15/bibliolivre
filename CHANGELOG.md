# Changelog

Formato inspirado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/) e [SemVer](https://semver.org/lang/pt-BR/).

## [1.0.0] — candidata à release (publicação pendente)

### Adicionado
- Pipeline de CI com lint, testes e cobertura em Python 3.10–3.12, harness Docker e artefatos de cobertura.
- Workflow CodeQL e dependências opcionais de desenvolvimento (`coverage.py` e Ruff).
- Seção As-Built na SPEC, evidência local reproduzível e roteiro de apresentação de 3–5 minutos.
- `.dockerignore` e volume nomeado para dados persistentes no Compose.

### Corrigido
- Colisão de unicidade do e-mail sentinela durante anonimização, com teste de regressão.
- Dependência TOML explícita para coverage.py em Python 3.10, identificada na primeira execução do CI.
- Tipos e imports identificados pelo Ruff.
- URLs, documentação de governança e afirmações de testes que não estavam comprovadas.

### Validação local
- 47 testes aprovados; 100% de cobertura de linhas em 348 instruções executáveis; Ruff aprovado.
- Execução Docker/CI remota e publicação da tag `v1.0.0` continuam pendentes até validar o PR e a revisão humana.

## Histórico acadêmico anterior (não são releases SemVer publicadas)

### Entrega 2
- Incluiu anonimização de membro (LGPD), transações SQLite `BEGIN IMMEDIATE`, testes de concorrência e propriedades, documentação técnica e roteiro inicial.
- O rótulo `2.0.0` que existia em uma versão anterior do changelog era um número de etapa acadêmica, não uma tag/release publicada, e foi removido para alinhar o versionamento do pacote.

### Entrega 1
- Incluiu a especificação inicial, arquitetura em camadas, cadastro, empréstimo, devolução, renovação, multas e harness de testes.
