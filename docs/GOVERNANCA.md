# Governança do Repositório

## Estado verificado no GitHub

Consulta realizada em 24 de outubro de 2026, antes da abertura do PR de preparação da release:

- Repositório: [`dantasz15/bibliolivre`](https://github.com/dantasz15/bibliolivre).
- A branch padrão configurada então era `devevop` (grafia existente no repositório); `main` também existia e apontava para a linha de release.
- `main` estava protegida para atores sujeitos à regra: PR e uma aprovação configurados; push forçado e exclusão estavam desabilitados. A configuração não aplicava a regra a administradores (`enforce_admins=false`), portanto um administrador pode ter possibilidade técnica de bypass.
- A proteção consultada não listava status checks obrigatórios. Portanto, CI configurado não deve ser descrito como bloqueio automático de merge enquanto essa regra remota não for atualizada.
- Não havia PR aberto antes desta preparação; o histórico público também não comprovava aprovações de code review, Project Board ou divisão de tarefas entre integrantes.
- O histórico inicial tinha uma branch de desenvolvimento chamada `devevop`; não há branch `develop` comprovada.

Este retrato descreve a configuração consultada, não uma afirmação de que todos os merges históricos cumpriram um fluxo de revisão. As alterações da Entrega 3 devem ser avaliadas no PR e sua situação final atualizada com dados reais.

## Fluxo de contribuição esperado

1. Criar uma branch de trabalho a partir de `main` atualizada.
2. Relacionar mudança funcional com SPEC e teste; mudanças de comportamento exigem teste de regressão.
3. Executar `make lint`, `make coverage` e o harness Docker quando houver engine disponível.
4. Abrir Pull Request para `main` com resumo e resultados reproduzíveis.
5. Aguardar CI verde e uma aprovação independente, conforme a proteção existente. O autor não pode aprovar o próprio PR.
6. Corrigir comentários e só então integrar usando o método permitido pelo GitHub.
7. Criar tag/release após a integração e verificar se não restaram PRs de release abertos.

A branch `release/1.0.0` desta entrega deve passar por esse fluxo. A exigência de revisão humana não será contornada por push direto, alteração para remover a regra ou aprovação simulada por IA.

## Evidências e limitações

Os arquivos de configuração versionados (`.github/workflows/`, `.github/CODEOWNERS` e o template de PR) descrevem os controles pretendidos. Eles não provam que o GitHub os executou nem que alguém aprovou uma alteração. Resultados CI, CodeQL, revisores, merge e release devem ser citados somente por seus links e estados observados na plataforma.

O PR da release não altera a ausência de registro histórico de Project Board ou de revisão por pares nas entregas anteriores. O projeto está documentado como trabalho individual de Gabriel Henrique Rodrigues Dantas; uma aprovação independente para o PR atual ainda está pendente.

## Estado da candidata à release — 25 de outubro de 2026

O [PR #9](https://github.com/dantasz15/bibliolivre/pull/9), branch `release/1.0.0` → `main`, foi verificado em draft no commit de implementação e workflows `fd8d14d` (`fd8d14dc0ae63bafaf5af42cbacb5612b9699a95`). As 12 verificações passaram: [CI do PR](https://github.com/dantasz15/bibliolivre/actions/runs/40212926287) e [CodeQL v4](https://github.com/dantasz15/bibliolivre/actions/runs/40212926292). A decisão remota continua `REVIEW_REQUIRED`, não há revisor atribuído e não houve merge nem tag `v1.0.0`.
