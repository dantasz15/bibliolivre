# Instruções para agentes de IA — BiblioLivre (Codex CLI e agentes compatíveis com AGENTS.md)

## Fluxo obrigatório (Spec-Driven Development)
1. **Leia `docs/SPEC.md` antes de qualquer alteração.** Ela é a fonte da verdade.
2. Nunca invente regra de negócio. Se a SPEC for ambígua, PARE e pergunte; sugira o texto da alteração da SPEC em vez de decidir sozinho.
3. Ordem de trabalho: SPEC → teste que falha → implementação → rodar a suíte.
4. Cite o ID da regra (RF-xx, RN-xx) em comentário no código e no nome/docstring do teste.

## Comandos
- Testes: `python -m unittest discover -s tests -t . -v`
- Testes no container: `docker compose run --rm test`
- Demonstração: `make demo`

## Arquitetura (não violar)
- `cli.py` → `services.py` → `repository.py` → SQLite. Regra de negócio só em `services.py`.
- `services.py` não imprime nada e não importa `argparse`.
- Datas: use sempre `self.hoje()`, nunca `date.today()` direto (ADR-004).
- Dinheiro: sempre `int` em centavos (ADR-005). Proibido `float` para valores.
- Escritas no banco: sempre dentro de `repo.transacao()` (ADR-006). Nunca use `with conn:`.
- Cobertura mínima de 95%: código novo sem teste reprova no CI.

## Segurança
- SQL **sempre** parametrizado com `?`. Proibido f-string/concatenação em SQL.
- Proibido adicionar dependências externas (RNF-01) sem ADR aprovado.
- Nunca ler, gerar ou commitar arquivos `*.db`, `.env` ou dados pessoais reais.
- Não execute comandos destrutivos (`rm -rf`, `git push --force`, `git reset --hard`, `DROP`) sem aprovação explícita.
- Não faça commit/push por conta própria; o humano revisa o diff e commita.

## Estilo
- Python ≥ 3.10, type hints, dataclasses imutáveis, mensagens de erro em português.
- Todo teste novo precisa cobrir ao menos um caso de borda.
