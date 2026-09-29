# Governança do Repositório

## Modelo de branches (Git Flow simplificado)
- `main` — versões entregues (tags `v1.0-entrega1`, `v2.0-entrega2`). **Protegida**: sem push direto; só recebe merge de `develop`.
- `develop` — integração contínua do trabalho da sprint. **Protegida**: só recebe PRs revisados.
- `feature/<issue>-<descricao>` — saem de `develop` e voltam para `develop` via PR (ex.: `feature/12-renovacao`).
- `fix/<issue>-<descricao>` — correções (ex.: `fix/18-multa-off-by-one`).
- `docs/<descricao>` — documentação.

## Regras de proteção da `main` e da `develop` (Settings → Branches / Rulesets)
- [x] Require a pull request before merging
- [x] Require approvals: **1** (revisor diferente do autor)
- [x] Require status checks to pass: `lint`, `test (3.10)`, `test (3.11)`, `test (3.12)`, `docker`, `analyze` (CodeQL)
- [x] Require conversation resolution before merging
- [x] Do not allow bypassing the above settings

## Critérios de aceitação para merge (Definition of Done)
1. CI verde: lint, testes nas três versões de Python com cobertura ≥ 95%, testes no Docker e CodeQL sem alertas.
2. Ao menos 1 aprovação de outro membro.
3. Toda regra nova/alterada tem teste e ID da SPEC citado.
4. Se o comportamento mudou, `docs/SPEC.md` foi atualizado **no mesmo PR**.
5. Código gerado por IA foi lido e entendido pelo autor e marcado no template do PR.
6. Sem segredos, dados pessoais reais ou arquivos `.db` no commit.

## Convenção de commits (Conventional Commits)
`feat:`, `fix:`, `test:`, `docs:`, `refactor:`, `ci:` — ex.: `fix(multa): não cobrar no dia do vencimento (#18)`.
Use `Closes #N` na descrição do PR para fechar a issue automaticamente.

## Planejamento em sprints
| Sprint | Objetivo | Issues sugeridas |
|---|---|---|
| 1 | Base do projeto | Estrutura do repo e CI · Modelos e erros · Repositório SQLite · Cadastro de livros/membros |
| 2 | Núcleo do domínio | Empréstimo (RN-01..04, 08) · Devolução e multa · Relógio injetável |
| 3 | Refinamento | Renovação · Listagem de atrasados · Pagamento de multas · CLI completa |
| 4 | Qualidade e entrega | Correções ERR-01..05 · Re-especificações RE-01..04 · README, ADRs, relatório de IA |

Use um **GitHub Project (Board)** com colunas *Backlog → Em andamento → Em revisão → Concluído* e um **Milestone** por sprint.

## Comandos úteis (GitHub CLI)
```bash
# issues, rótulos e milestones de todas as sprints
./scripts/criar_issues.sh usuario/repositorio

# rótulos (já incluídos no script)
gh label create spec --color 5319e7 --description "Mudança na especificação"
gh label create ia-assistido --color fbca04 --description "PR com código gerado/assistido por IA"

# fluxo de uma feature
git switch develop && git pull
git switch -c feature/12-renovacao
# ... código + testes ...
git commit -m "feat(renovacao): permite 1 renovação de 7 dias (RN-05) (#12)"
git push -u origin feature/12-renovacao
gh pr create --base develop --fill --reviewer <colega>
```

## Evidências a anexar na entrega
- Link da aba *Pull requests* (fechados) mostrando revisões com comentários.
- Link do *Insights → Contributors* e *Network*.
- Link do Project Board e dos Milestones fechados.
- Print da regra de proteção da `main`.
