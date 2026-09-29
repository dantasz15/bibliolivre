# Relato de Experiência

> Seção de comunicação técnica. Escrevam na primeira pessoa do plural, com exemplos reais. Os tópicos abaixo servem de roteiro (também servem para o vídeo curto, se o professor preferir: ~1 min por tópico).

## 1. O problema e a solução em uma frase
BiblioLivre substitui o caderno de empréstimos de bibliotecas comunitárias por um sistema offline que controla prazos e multas automaticamente.

## 2. Como nos organizamos
[PREENCHER: divisão de papéis, frequência de reuniões, ferramenta de comunicação, como usamos o Project Board.]

## 3. O que funcionou
- Escrever a SPEC com IDs (RN-xx) antes do código facilitou a divisão do trabalho e a rastreabilidade dos testes.
- O relógio injetável tornou triviais testes que seriam impossíveis ("30 dias depois").
- [PREENCHER]

## 4. Desafios
- Conflitos de merge quando duas pessoas mexeram em `services.py` ao mesmo tempo → [PREENCHER: como resolveram].
- Descobrir que a regra de bloqueio tinha uma brecha (RE-03) só depois dos testes de borda.
- [PREENCHER: dificuldades com Git, com as ferramentas de IA, com prazos.]

## 5. Aprendizados
- Testes de borda revelam erros de **especificação**, não só de código.
- IA acelera a parte mecânica, mas não substitui entender o domínio.
- Code review é mais eficiente com PRs pequenos.
- [PREENCHER: um aprendizado individual de cada membro.]

## 6. O que faríamos diferente
[PREENCHER]
