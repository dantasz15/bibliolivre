# Como contribuir

1. Confirme a situação das issues existentes no GitHub; não há Project Board configurado/documentado neste repositório.
2. Atualize sua cópia de `main` e crie uma branch curta, por exemplo `fix/<descricao>` ou `docs/<descricao>`.
3. Siga SDD: revise a SPEC, acrescente/ajuste o teste e implemente a mudança.
4. Rode `make lint` e `make coverage`. Se alterar o container, rode `docker compose run --build --rm test` e valide a imagem runtime.
5. Abra um Pull Request para `main` com resumo, requisitos afetados e evidências dos comandos.
6. Aguarde CI e CodeQL. Uma revisão independente é recomendada; a regra atual exige Pull Request, mas está configurada com zero aprovações obrigatórias em razão do trabalho individual.
7. Integre somente quando as regras remotas da branch estiverem satisfeitas.

O repositório é documentado como projeto individual. Nomes, papéis, reuniões e revisões só devem ser registrados quando ocorrerem de fato. A governança observada está em [`docs/GOVERNANCA.md`](docs/GOVERNANCA.md).
