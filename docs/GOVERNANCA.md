# Governança do Repositório

## Estado verificado no GitHub — 26 de outubro de 2026

- Repositório: [`dantasz15/bibliolivre`](https://github.com/dantasz15/bibliolivre).
- A branch padrão é `main`. Ela contém a Entrega Final integrada pelo [PR #9](https://github.com/dantasz15/bibliolivre/pull/9), fechado como merged em 26/10/2026.
- A regra de proteção de `main` exige Pull Request e se aplica também a administradores. O número de aprovações obrigatórias foi alterado para zero, por decisão expressa do autor em razão do trabalho individual. Push forçado e exclusão da branch permanecem desabilitados. A regra não configura checks de status obrigatórios; por isso, os checks verdes foram confirmados como evidência, mas não são condição automatizada da proteção.
- O PR #9 foi revisado pelo próprio autor, conforme a declaração de trabalho individual. Não houve aprovação independente registrada. Essa limitação não é apresentada como revisão por pares.
- O commit de merge em `main` é `6df47b8453967c3326b9dba40e780477a8452077`. Não havia Pull Requests abertos na verificação após a integração.
- A tag [`v1.0.0`](https://github.com/dantasz15/bibliolivre/releases/tag/v1.0.0) e a Release oficial foram publicadas a partir de `main`, apontando para o commit de merge `6df47b8`.
- O roteiro funcional está em [`ROTEIRO_APRESENTACAO.md`](ROTEIRO_APRESENTACAO.md). Até esta verificação, não havia link público informado para um vídeo gravado; não se apresenta o roteiro como gravação concluída.

## Validação automatizada da release

No head `e9771d6` do PR #9, a matriz de CI e o CodeQL concluíram com sucesso, totalizando 12 verificações aprovadas. A suíte passou com 47 testes em cada versão Python 3.10, 3.11 e 3.12 e 100% de cobertura de linhas em 348 instruções; o harness Docker também passou e a imagem runtime foi construída. Depois do merge, os workflows de CI e CodeQL foram executados novamente no commit `6df47b8` de `main` e terminaram com sucesso.

- [CI no commit integrado — execução 40414632362](https://github.com/dantasz15/bibliolivre/actions/runs/40414632362).
- [CodeQL no commit integrado — execução 40414632359](https://github.com/dantasz15/bibliolivre/actions/runs/40414632359).
- Runs anteriores do PR e detalhes dos artefatos de cobertura estão em [`docs/TESTES.md`](TESTES.md), sujeitos ao prazo de retenção do GitHub Actions.

A aprovação dos checks atesta somente as verificações automatizadas executadas. Ela não constitui aprovação independente nem prova ausência de defeitos.

## Fluxo para mudanças futuras

1. Criar uma branch a partir de `main` atualizada.
2. Relacionar mudanças funcionais à SPEC e a testes; mudanças de comportamento precisam de teste de regressão.
3. Executar `make lint`, `make coverage` e o harness Docker.
4. Abrir Pull Request para `main` com resumo e evidências reproduzíveis.
5. Aguardar CI e CodeQL verdes. Uma revisão independente continua sendo recomendada para mudanças futuras, ainda que o número obrigatório de aprovações esteja configurado como zero.
6. Corrigir comentários e integrar pelo fluxo de Pull Request; não usar push direto para contornar a proteção.
7. Para mudanças posteriores à versão 1.0.0, seguir o versionamento SemVer e publicar uma nova release quando houver alteração de produto que a justifique.

## Encerramento da Entrega Final

O código foi integrado em `main`, a branch padrão foi alinhada para `main`, a proteção com exigência de Pull Request foi mantida, não há PR de release aberto e a release `v1.0.0` está publicada. Permanece como etapa acadêmica a gravação e publicação de uma demonstração funcional de 3–5 minutos, com atualização do PDF e inclusão do link verificável quando disponível.
