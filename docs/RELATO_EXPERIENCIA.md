# Retrospectiva Técnica do Projeto

## 1. Problema e solução

O BiblioLivre substitui o registro manual de empréstimos em bibliotecas comunitárias por uma CLI offline que organiza acervo, membros, empréstimos, prazos, multas, devoluções e renovações em SQLite local.

## 2. Organização e governança observadas

O repositório identifica Gabriel Henrique Rodrigues Dantas como autor individual. O histórico público inicial contém um commit de estrutura e não registra divisão de tarefas entre integrantes, reuniões, Project Board, PRs de feature ou revisão por pares. Portanto, esta retrospectiva não atribui atividades a uma equipe nem declara reuniões ou processos que não estejam comprovados.

Para esta preparação da release, as alterações estão isoladas em uma branch de release, com testes, documentação e CI propostos em conjunto. A proteção da `main` exige um PR e uma aprovação independente; até que essa revisão ocorra, a release não está incorporada à branch principal.

## 3. Resultados reproduzidos

- A suíte final local executou 47 testes e terminou sem falhas.
- `coverage.py` mediu 100% de cobertura de linhas nos módulos incluídos, totalizando 348 instruções executáveis nessa execução.
- Ruff não encontrou problemas no código e nos testes.
- O cenário `make demo` concluiu cadastro de livro e membro, empréstimo, renovação, devolução e anonimização.
- A imagem e os testes Docker ainda dependem da execução do workflow no GitHub, pois o ambiente de desenvolvimento utilizado não dispunha de Docker.

## 4. Desafios e correções

Durante a auditoria de fechamento foi encontrado um caso não coberto: a anonimização podia tentar gravar um e-mail sentinela já usado por outro membro, violando a restrição `UNIQUE`. A implementação foi ajustada para procurar um sufixo livre e um teste de regressão foi adicionado. A situação ilustra que uma suíte verde cobre os casos escritos, não todas as combinações possíveis.

Também foram corrigidas instruções de build Docker para usar volume nomeado e foi adicionado `.dockerignore`, evitando que arquivos locais e dados desnecessários sejam enviados no contexto de build.

## 5. Aprendizados apoiados por evidências

- Manter a SPEC explícita ajuda a rastrear as regras, mas o As-Built precisa ser conferido contra o código e a API efetivos.
- Testes de regressão transformam um achado de revisão em uma proteção repetível.
- Cobertura de 100% de linhas não é sinônimo de ausência de bugs: o caso de colisão só apareceu na auditoria de combinações de dados.
- A CI e a execução Docker são importantes para validar mais de uma versão de Python e o ambiente empacotado; essa evidência ainda precisa vir do GitHub Actions.
- Revisão humana independente não pode ser substituída por IA ou pela aprovação dos testes.

## 6. Próximos passos para encerrar

Aprovar e incorporar o PR na `main`, confirmar os status de CI e CodeQL, publicar a tag/release `v1.0.0`, alterar a branch padrão para `main` se aprovado pelo mantenedor, gravar a demonstração de 3–5 minutos e anexar o link real ao PDF acadêmico. Não foram estimadas horas economizadas nem experiências de equipe porque não há registros que sustentem esses dados.