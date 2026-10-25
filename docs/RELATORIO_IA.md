# Relatório Técnico-Ético: Uso de IA no BiblioLivre

## 1. Evidências e escopo da análise

O autor forneceu uma conversa compartilhada com Claude como contexto do projeto. O repositório público contém arquivos de instrução para Claude Code, Codex CLI e Cursor, mas esses arquivos não provam que os três produtos tenham sido executados. Não há logs versionados de prompts, versões/modelos, tempo economizado, respostas rejeitadas ou quantidade de correções por ferramenta. Por isso, este relatório não atribui notas comparativas nem inventa métricas de produtividade.

Nesta preparação de release, uma revisão assistida por IA identificou que a anonimização podia falhar se outro membro já tivesse cadastrado o e-mail sentinela previsível. Foi acrescentado o teste `test_colisao_de_email_sentinela_nao_impede_anonimizacao`, e o repositório procura um sufixo disponível antes de atualizar o membro. Esse é um exemplo observável de valor de revisão e também da necessidade de transformar achados em regressões automatizadas.

## 2. Benefícios e limites observáveis

O projeto tem uma SPEC com IDs de requisitos, 47 testes automatizados e uma execução local de cobertura. A estrutura permite verificar relações entre regras, código e testes. A existência desses artefatos não permite afirmar quanto tempo a IA economizou ou que uma ferramenta específica escreveu cada módulo. Também não houve comparação controlada entre Claude Code, Codex CLI, Cursor e Antigravity.

Um modelo pode sugerir código plausível que não cobre todos os casos de borda, pode produzir premissas incorretas ou declarar sucesso sem executar os testes. Uma resposta gerada não substitui a leitura do diff, a execução do test harness nem a validação humana das regras de negócio.

## 3. Segurança, privacidade e dados pessoais

O sistema armazena nome e e-mail de membros. O repositório implementa anonimização, mas essa função, isoladamente, não comprova conformidade completa com a LGPD, que depende de finalidade, base legal, retenção, atendimento de direitos e responsabilidades do controlador. Bases reais, dados pessoais, credenciais e arquivos `.env` não devem ser enviados a modelos nem incluídos no Git.

O código usa consultas SQL parametrizadas e transações SQLite `BEGIN IMMEDIATE`. A imagem Docker exclui arquivos locais sensíveis do contexto e executa como usuário não-root. Esses controles reduzem riscos conhecidos, mas não equivalem a uma auditoria de segurança abrangente.

## 4. Propriedade intelectual e transparência

A origem e a licença de código incorporado devem ser verificadas. A presença de uma licença no repositório não substitui a conferência de dependências, trechos de terceiros ou termos das ferramentas utilizadas. A autoria, a declaração de assistência por IA e as regras acadêmicas devem ser tratadas de acordo com as orientações da instituição; este documento não oferece conclusão jurídica sobre titularidade de código gerado.

## 5. Homologação humana no fluxo SDD

A SPEC registra o comportamento esperado; os testes verificam apenas os cenários codificados. Mesmo 100% de cobertura de linhas não prova que todos os requisitos estejam corretos, completos ou bem interpretados. A homologação requer leitura da especificação e do diff, execução dos testes e confirmação de que os fluxos atendem ao problema real.

O trabalho está documentado como individual. O histórico inicial do GitHub não comprova revisão por pares; a branch `main` está protegida e requer uma aprovação independente para incorporar este PR de release. Essa aprovação deve vir de uma pessoa real, não do agente de IA nem do autor do PR.

## 6. Conclusão

A IA pode ser usada como apoio para análise, implementação e revisão, desde que seus resultados sejam tratados como propostas. O dado concreto deste fechamento é a detecção de um conflito de unicidade na anonimização, coberto por teste de regressão. Não há evidência suficiente para quantificar produtividade ou comparar ferramentas; alegações desse tipo foram omitidas. A decisão final sobre requisitos, revisão e homologação permanece humana.