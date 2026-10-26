# Configuração e Uso de Agentes de IA no Fluxo SDD

## Arquivos de instrução presentes

| Ferramenta | Arquivo no repositório | O que a presença do arquivo comprova |
|---|---|---|
| Claude Code | `CLAUDE.md` | Há instruções de contexto para orientar a ferramenta; não comprova execução. |
| Codex CLI | `AGENTS.md` | Há instruções para agentes compatíveis; não comprova execução. |
| Cursor | `.cursorrules` e `.cursorignore` | Há regras e exclusões de contexto; não comprova uso do editor. |
| Antigravity | Sem configuração ou log específico | Não avaliado como ferramenta utilizada. |

Os arquivos de instrução recomendam manter `docs/SPEC.md` como referência, criar testes antes das alterações e revisar o código. Eles são artefatos de configuração, não registros de prompts, execuções, versões de modelo ou aprovações.

## Fluxo recomendado de trabalho

1. A pessoa responsável define e aprova os requisitos da SPEC.
2. A ferramenta pode sugerir cenários de teste e alterações; a pessoa revisa ambos.
3. A suíte é executada em ambiente reproduzível; o resultado observado, e não a afirmação do agente, é a evidência.
4. O autor lê o diff e documenta mudanças relevantes.
5. Para incorporar em `main`, a proteção atual do GitHub exige PR e uma aprovação de outra pessoa.

Esse fluxo é a prática recomendada. O histórico público inicial não contém PRs de código com revisão humana, divisão de tarefas, reuniões ou Project Board que comprovem que ele foi seguido nas entregas anteriores.

## Evidência de uso disponível e limites

O autor forneceu uma conversa compartilhada com Claude como contexto do projeto. O repositório não contém registro completo de prompts, versões de modelos, ferramentas de terminal executadas, tempo economizado ou taxas de retrabalho. A existência de arquivos como `CLAUDE.md`, `AGENTS.md` e `.cursorrules` não permite concluir que Claude Code, Codex CLI ou Cursor foram executados.

Na preparação desta release, a revisão assistida por IA identificou uma colisão possível do e-mail sentinela de anonimização com a restrição `UNIQUE`; foi acrescentado um teste de regressão e a implementação passou a procurar um sufixo livre. Esse achado e sua correção estão no histórico de trabalho desta branch; a incorporação na `main` ainda depende de revisão humana.

## Controles de segurança

- Não enviar base SQLite real, e-mail/nome de membro, credenciais, `.env` ou logs pessoais a serviços externos.
- Validar código sugerido contra SPEC, testes, parametrização SQL e revisão do diff.
- Não executar comandos destrutivos nem publicar dados sem entender seu efeito.
- Tratar cobertura como medida de linhas executadas, não como garantia de ausência de defeitos.

Não há comparação controlada entre ferramentas, pontuação de qualidade ou estimativa de produtividade neste relatório porque não existem registros comparáveis suficientes.