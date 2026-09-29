#!/usr/bin/env sh
# Cria rótulos, milestones e issues das sprints no GitHub (requer: gh auth login)
# Uso: ./scripts/criar_issues.sh <usuario/repositorio>
set -e
R="$1"; [ -z "$R" ] && { echo "uso: $0 usuario/repo"; exit 1; }

gh label create spec        -R "$R" --color 5319e7 --description "Mudança na especificação" || true
gh label create ia-assistido -R "$R" --color fbca04 --description "Código gerado/assistido por IA" || true
gh label create teste       -R "$R" --color 0e8a16 --description "Test harness" || true

for m in "Sprint 1 - Ambiente e SPEC" "Sprint 2 - Núcleo do domínio" "Sprint 3 - Refinamento" "Sprint 4 - Entrega final"; do
  gh api "repos/$R/milestones" -f title="$m" >/dev/null || true
done

i() { gh issue create -R "$R" --title "$1" --body "$2" --label "$3" --milestone "$4"; }
S1="Sprint 1 - Ambiente e SPEC"; S2="Sprint 2 - Núcleo do domínio"; S3="Sprint 3 - Refinamento"; S4="Sprint 4 - Entrega final"

i "Estrutura do repositório, branches e proteção" "main/develop protegidas, templates de PR/issue, CODEOWNERS" documentation "$S1"
i "Especificação técnica v1.0 (docs/SPEC.md)" "Problema, RF, RNF, RN, contratos de E/S e decomposição em unidades" spec "$S1"
i "Configurar agentes de IA (CLAUDE.md, AGENTS.md, .cursorrules)" "Ver docs/AGENTES_IA.md" documentation "$S1"
i "Ambiente padronizado (Dockerfile, docker-compose, Makefile)" "Reprodutibilidade" enhancement "$S1"
i "Test harness + CI (GitHub Actions)" "unittest, Relogio falso, SQLite em memória, logs em docs/evidencias" teste "$S1"
i "U1/U2 Entidades e exceções" "models.py, errors.py" enhancement "$S1"
i "U3 Validação de ISBN-13 (RF-01)" "Dígito verificador, hífens" enhancement "$S2"
i "U5 Repositório SQLite" "SQL parametrizado (RNF-04)" enhancement "$S2"
i "U6 Cadastro de livros e membros (RF-01, RF-02)" "" enhancement "$S2"
i "U4 Cálculo de multa (RN-06)" "Função pura, centavos" enhancement "$S2"
i "U7 Empréstimo e devolução (RN-01..04, RN-08)" "" enhancement "$S2"
i "Renovação (RN-05)" "" enhancement "$S3"
i "Listagem de atrasados e pagamento de multas (RF-06, RF-07)" "" enhancement "$S3"
i "U8 CLI completa" "Contrato da seção 5.2 da SPEC" enhancement "$S3"
i "README final, ADRs, relatório de IA" "" documentation "$S4"
echo "Pronto."
