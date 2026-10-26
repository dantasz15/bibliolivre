# Retrospectiva Técnica do Projeto

## 1. Problema e solução

O BiblioLivre substitui o registro manual de empréstimos em bibliotecas comunitárias por uma CLI offline que organiza acervo, membros, empréstimos, prazos, multas, devoluções e renovações em SQLite local.

## 2. Organização e governança observadas

O repositório identifica Gabriel Henrique Rodrigues Dantas como autor individual. O histórico público inicial contém um commit de estrutura e não registra divisão de tarefas entre integrantes, reuniões, Project Board, PRs de feature ou revisão por pares. Portanto, esta retrospectiva não atribui atividades a uma equipe nem declara reuniões ou processos que não estejam comprovados.

O PR #9 da branch `release/1.0.0` foi integrado em `main` em 26/10/2026 e originou a release oficial `v1.0.0`. O autor revisou o próprio PR por se tratar de trabalho individual e autorizou configurar zero aprovações obrigatórias; a regra de Pull Request foi mantida. Não houve aprovação independente registrada, e isso é tratado como limite de governança, não como revisão por pares.

## 3. Resultados reproduzidos

- A suíte final local executou 47 testes e terminou sem falhas.
- `coverage.py` mediu 100% de cobertura de linhas nos módulos incluídos, totalizando 348 instruções executáveis nessa execução.
- Ruff não encontrou problemas no código e nos testes.
- O cenário `make demo` concluiu cadastro de livro e membro, empréstimo, renovação, devolução e anonimização.
- O ambiente local não dispunha de Docker; no GitHub Actions, o harness Docker executou 47 testes e o build da imagem runtime passou no head validado do PR #9 (`c099ba1`).

## 4. Desafios e correções

Durante a auditoria de fechamento foi encontrado um caso não coberto: a anonimização podia tentar gravar um e-mail sentinela já usado por outro membro, violando a restrição `UNIQUE`. A implementação foi ajustada para procurar um sufixo livre e um teste de regressão foi adicionado. A situação ilustra que uma suíte verde cobre os casos escritos, não todas as combinações possíveis.

Também foram corrigidas instruções de build Docker para usar volume nomeado e foi adicionado `.dockerignore`, evitando que arquivos locais e dados desnecessários sejam enviados no contexto de build.

## 5. Aprendizados apoiados por evidências

- Manter a SPEC explícita ajuda a rastrear as regras, mas o As-Built precisa ser conferido contra o código e a API efetivos.
- Testes de regressão transformam um achado de revisão em uma proteção repetível.
- Cobertura de 100% de linhas não é sinônimo de ausência de bugs: o caso de colisão só apareceu na auditoria de combinações de dados.
- A CI validou 47 testes em cada versão Python 3.10–3.12, cobertura de 100% em 348 instruções, Docker e CodeQL v4 no PR #9; depois do merge, CI e CodeQL também passaram no commit `6df47b8` de `main`, conforme `docs/TESTES.md`.
- Revisão humana independente não pode ser substituída por IA ou pela aprovação dos testes.

## 6. Etapa acadêmica remanescente

A release técnica `v1.0.0` está publicada e a branch padrão é `main`. Para concluir a submissão acadêmica, falta gravar e publicar a demonstração funcional de 3–5 minutos e acrescentar ao PDF o link verificável quando disponível. Não foram estimadas horas economizadas nem experiências de equipe porque não há registros que sustentem esses dados.
