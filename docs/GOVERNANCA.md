# Governança do Repositório

## Estado verificado no GitHub — 26 de outubro de 2026

- Repositório: [`dantasz15/bibliolivre`](https://github.com/dantasz15/bibliolivre).
- Branch padrão atual: `devevop`. A branch `main` existe, mas ainda não é a branch padrão.
- `main` está protegida e exige Pull Request e uma aprovação. Push forçado e exclusão estão desabilitados. Em 26/10/2026, a aplicação da regra a administradores foi ativada (`enforce_admins=true`). A configuração ainda não lista checks obrigatórios (`required_status_checks=null`). Assim, os workflows verdes são evidência de validação, mas a regra de proteção consultada não os exige para permitir merge.
- `main` aponta para `369bbf10eb5b7e0af0c23aa61459afc0e160dda0`. A branch `release/1.0.0` aponta para `868d9b06b4ac657d5ace21855720a67448f2c43b`.
- O [PR #9](https://github.com/dantasz15/bibliolivre/pull/9), de `release/1.0.0` para `main`, está aberto e pronto para revisão. O estado é `REVIEW_REQUIRED`/`BLOCKED`, não há revisor solicitado e o PR não foi integrado.
- Não há tags Git nem releases publicadas no repositório. A tag `v1.0.0` ainda não existe.
- O histórico inicial identifica o trabalho como individual; não há evidência de divisão de tarefas, reuniões, Project Board ou revisão por pares nas etapas anteriores.

## Validação automatizada da candidata

No head `868d9b06b4ac657d5ace21855720a67448f2c43b`, a página do PR reportou 12 checks aprovados, sem falhas ou pendências. A CI executou lint, 47 testes em Python 3.10, 3.11 e 3.12, cobertura de 100% em 348 instruções e o harness/build Docker. A análise CodeQL v4 também passou. Links para os runs e detalhes estão em [`docs/TESTES.md`](TESTES.md).

Checks aprovados não substituem a aprovação humana exigida pela regra do PR, não incorporam automaticamente o código e não criam uma tag/release.

## Fluxo de contribuição

1. Criar uma branch a partir de `main` atualizada.
2. Relacionar mudanças funcionais à SPEC e a testes; mudanças de comportamento precisam de teste de regressão.
3. Executar `make lint`, `make coverage` e o harness Docker.
4. Abrir Pull Request para `main` com resumo e evidências reproduzíveis.
5. Aguardar checks verdes e aprovação de uma pessoa diferente do autor.
6. Corrigir comentários e integrar pelo fluxo aprovado no GitHub, sem contornar a proteção.
7. Depois do merge, publicar a tag/release e verificar se não restaram PRs de release abertos.

A exigência de revisão independente não será contornada por push direto, aprovação simulada por IA ou mudança de proteção feita para liberar este PR.

## Pendências para a Entrega Final

Para declarar a release final concluída, ainda é necessário obter revisão independente do PR #9, integrá-lo em `main`, criar e publicar `v1.0.0`, confirmar a versão final na branch padrão e gravar/publicar a demonstração funcional de 3–5 minutos. Depois, atualizar o PDF e esta documentação com os links definitivos. Até lá, o estado correto é **candidata à release**, não release concluída.
