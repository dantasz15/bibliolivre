# Passo a passo para publicar o projeto (Entregas 1 e 2)

O histórico de commits, PRs e revisões precisa ser **feito de verdade pelo grupo**. Não alterem datas de commit nem simulem revisões: o GitHub registra quando cada ação ocorreu e isso é fácil de verificar.

## 1. Criar o repositório (líder)
```bash
gh repo create bibliolivre --public --clone
cd bibliolivre
# copie para cá APENAS: README.md, LICENSE, .gitignore, .github/
git add . && git commit -m "chore: estrutura inicial do repositório"
git push -u origin main
git switch -c develop && git push -u origin develop
```
Depois: Settings → Branches → proteger `main` e `develop` (ver `docs/GOVERNANCA.md`), adicionar colegas como colaboradores e dar acesso aos professores.

## 2. Criar issues e o Project Board
```bash
./scripts/criar_issues.sh usuario/bibliolivre
```
Crie um Project (Board), adicione as issues e atribua cada uma a um membro.

## 3. Entregar cada parte por PR (cada membro faz as suas)
Para cada issue, na ordem da seção 6 da SPEC:
```bash
git switch develop && git pull
git switch -c feature/<n>-<nome>
# copiar os arquivos daquela unidade + seus testes, LER e ENTENDER o código
./scripts/run_tests.sh
git add . && git commit -m "feat: <descrição> (#<n>)"
git push -u origin feature/<n>-<nome>
gh pr create --base develop --fill --reviewer <colega>
```
O revisor deve comentar de verdade (dúvidas, sugestões) antes de aprovar.

Ordem sugerida de PRs (Entrega 1): SPEC + agentes + Docker → models/errors → services + repository + helpers + test_cadastro → test_emprestimos → CLI + test_cli → docs.

Entrega 2: correções ERR-06/ERR-07 (transações + `test_lgpd_concorrencia.py`) → RF-09 LGPD → `test_propriedades.py` → CI com lint/cobertura/CodeQL/Dependabot → SECURITY, CHANGELOG, ADR-006/007 → relatório de IA e roteiro.

## 4. Fechar a Entrega 1
```bash
git switch main && git merge --no-ff develop   # via PR develop → main
git tag v1.0-entrega1 && git push --tags
./scripts/run_tests.sh                         # e: docker compose run --rm test
```
Tire prints de: Actions verde, execução no Docker, lista de PRs, Project Board. Cole no PDF de submissão.

## 5. Entrega 2
Continue nas sprints 3 e 4; os erros e re-especificações do `ERROS_E_RE_ESPECIFICACAO.md` viram issues `bug`/`spec` com PRs próprios. Ao final, tag `v2.0-entrega2`.
