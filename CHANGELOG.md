# Changelog
Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/) e [SemVer](https://semver.org/lang/pt-BR/).

## [2.0.0] — Entrega 2
### Adicionado
- RF-09: anonimização de membro (LGPD) — comando `membro-anonimizar`.
- RNF-07: transações atômicas com `BEGIN IMMEDIATE` (ADR-006).
- Testes de propriedade (simulação aleatória com invariantes) e de concorrência.
- CI com lint (Ruff), cobertura mínima de 95%, testes no Docker; CodeQL; Dependabot.
- SECURITY.md, CHANGELOG.md, roteiro de apresentação.
### Corrigido
- ERR-06: dois empréstimos simultâneos do último exemplar.
- ERR-07: banco corrompido exibia stack trace na CLI.
- ERR-01 a ERR-05 (ver `docs/ERROS_E_RE_ESPECIFICACAO.md`).
### Alterado
- SPEC v1.1 → v1.2 (RE-01 a RE-05).

## [1.0.0] — Entrega 1
### Adicionado
- SPEC v1.0, arquitetura em camadas, cadastro, empréstimo, devolução, renovação, multas.
- Test harness (unittest + relógio falso), Docker, docker-compose, arquivos de agentes de IA.
