# Como contribuir

1. Pegue uma issue no Project Board e atribua a você.
2. `git switch -c feature/<n>-<descricao>` a partir da `main` atualizada.
3. Ordem SDD: atualize a SPEC (se necessário) → escreva o teste → implemente.
4. `make test` localmente.
5. Abra o PR usando o template e peça revisão a um colega.
6. Revisor: rode os testes, leia o diff inteiro, comente, aprove ou peça mudanças.
7. Merge com *Squash and merge* após CI verde + aprovação.

Regras completas em [`docs/GOVERNANCA.md`](docs/GOVERNANCA.md).
