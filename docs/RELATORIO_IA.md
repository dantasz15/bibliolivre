# Relatório Técnico-Ético: Uso de Agentes de IA no Ciclo de Vida do Software

> Este relatório deve refletir a experiência **real** do grupo. Os trechos marcados com [PREENCHER] precisam dos exemplos concretos de vocês (prompts usados, erros que a ferramenta cometeu, tempo economizado ou perdido). A análise geral abaixo serve de base e pode ser mantida.

## 1. Metodologia
Cada ferramenta foi usada em pelo menos uma destas tarefas: (a) transformar a SPEC em esqueleto de código, (b) gerar testes a partir das regras RN-xx, (c) encontrar e corrigir um bug real (ERR-01 ou ERR-03), (d) revisar um PR. Avaliamos qualidade do resultado, quantidade de correções humanas necessárias e aderência à SPEC.

| Ferramenta | Quem usou | Tarefas | Versão/modelo |
|---|---|---|---|
| Claude Code | [PREENCHER] | [PREENCHER] | [PREENCHER] |
| Codex CLI | [PREENCHER] | [PREENCHER] | [PREENCHER] |
| Cursor | [PREENCHER] | [PREENCHER] | [PREENCHER] |
| Antigravity | [PREENCHER] | [PREENCHER] | [PREENCHER] |

## 2. Matriz comparativa
Escala 1 (fraco) a 5 (forte). **Ajustem as notas à experiência do grupo** — as abaixo são um ponto de partida baseado nas características gerais de cada ferramenta.

| Critério | Claude Code | Codex CLI | Cursor | Antigravity |
|---|---|---|---|---|
| Interface | Agente no terminal | Agente no terminal | IDE (fork do VS Code) | IDE agent-first |
| Compreensão do repositório inteiro | 5 | 4 | 4 | 4 |
| Aderência à SPEC quando ela é fornecida | [ ] | [ ] | [ ] | [ ] |
| Qualidade dos testes gerados (bordas) | [ ] | [ ] | [ ] | [ ] |
| Execução autônoma (roda testes, corrige) | 5 | 4 | 3 | 5 |
| Edição fina / autocomplete no editor | 2 | 2 | 5 | 4 |
| Controle humano (aprovação de cada ação) | 4 | 4 | 5 | 3 |
| Tendência a alucinar APIs/funções | [ ] | [ ] | [ ] | [ ] |
| Curva de aprendizado | média | média | baixa | média |

### Pontos fortes e limitações observados
**Claude Code** — Forte em tarefas de várias etapas: lê a SPEC, cria arquivos, roda os testes e itera até passarem. Limitação: por agir com autonomia, pode editar vários arquivos de uma vez; exige ler o diff inteiro antes de commitar. [PREENCHER: exemplo real]

**Codex CLI** — Fluxo parecido no terminal, com modos de aprovação configuráveis e execução em sandbox. Limitação: [PREENCHER].

**Cursor** — Melhor para edição incremental dentro do editor e para quem prefere revisar linha a linha. Limitação: o contexto depende dos arquivos que você referencia; sem a SPEC anexada, tende a "inventar" regras plausíveis. [PREENCHER]

**Antigravity** — Orienta o trabalho em torno de agentes que planejam e executam tarefas, produzindo artefatos (planos, capturas) para revisão. Limitação: [PREENCHER].

## 3. Impacto real na qualidade
- **Especificação:** a IA foi útil para encontrar ambiguidades (ex.: perguntar "renovar no dia do vencimento conta?" levou à RE-01). Porém, quando pedimos para "completar a especificação", ela inventou regras não pedidas pelo cliente — toda regra sugerida por IA passou por decisão da equipe.
- **Código:** acelerou o boilerplate (repositório SQLite, argparse). Os erros de lógica de domínio (ERR-01 off-by-one, RE-03 brecha de bloqueio) **não** foram detectados espontaneamente pela IA; foram revelados pelos testes de borda escritos a partir da SPEC.
- **Testes:** as ferramentas geram muitos testes do "caminho feliz". Os casos de fronteira (dia 0, dia 40/41 do teto, `True` como inteiro) exigiram orientação humana explícita.

## 4. Ética, limites e segurança

### 4.1 Alucinação e código inseguro ou destrutivo
- **Exemplo real deste projeto:** a CLI abria o banco fora do bloco de tratamento de erros (ERR-07). O código "parecia certo" e passava nos testes existentes; só um teste de borda escrito pensando no pior caso revelou o stack trace exposto. Código plausível não é código correto.
- **Alucinação:** modelos podem citar funções ou parâmetros que não existem, ou "confirmar" que um teste passa sem executá-lo. Mitigação: CI obrigatório — só vale o resultado da pipeline, nunca a afirmação da ferramenta.
- **Código inseguro:** o padrão mais comum é SQL montado com f-string. Adotamos RNF-04 (SQL sempre parametrizado) e um teste de injeção (`test_sql_injection_tratado_como_texto`).
- **Concorrência:** agentes tendem a gerar código correto para um usuário só. A condição de corrida ERR-06 só aparece com execução simultânea, e a IA não a apontou espontaneamente.
- **Ações destrutivas:** agentes com acesso ao terminal podem executar `rm -rf`, `git push --force`, `DROP TABLE` ou apagar o banco para "resolver" um erro. Mitigações: modo de aprovação manual para comandos, nunca rodar agente com credenciais de produção, `main` protegida contra force-push.
- **Dependências inventadas (slopsquatting):** a IA pode sugerir pacotes inexistentes cujo nome um atacante registra depois. Nosso RNF-01 (zero dependências) elimina esse risco neste projeto; em outros, verificar cada pacote no PyPI antes de instalar.

### 4.2 Vazamento de dados, privacidade e confidencialidade
- Tudo o que entra no contexto (código, `.env`, banco, logs) pode ser enviado ao provedor do modelo. Dependendo do plano e das configurações, pode ser retido ou usado para treinamento.
- Dados de membros (nome, e-mail) são **dados pessoais pela LGPD**. Regra do grupo: nunca colar o `bibliolivre.db` real ou dados reais em prompts; usar apenas dados fictícios. `.gitignore` exclui `*.db` e `.env`.
- **Consequência concreta no projeto:** essa discussão gerou a re-especificação RE-05 e o RF-09 (anonimização a pedido do titular, LGPD art. 18). O relatório ético não ficou só no papel: virou requisito, teste e código.
- Em contexto profissional: verificar termos de uso, preferir planos corporativos com retenção zero, e configurar arquivos de exclusão de contexto (ex.: `.cursorignore`) para segredos.

### 4.3 Propriedade intelectual e direitos autorais
- A autoria de código gerado por IA ainda é juridicamente incerta: em vários países, obra sem autoria humana significativa pode não ser protegida por direito autoral. No Brasil, a Lei 9.610/98 pressupõe autor pessoa física, e o tema está em discussão legislativa.
- Risco de o modelo reproduzir trechos de código com licença restritiva (ex.: GPL) sem atribuição. Mitigação: não aceitar blocos grandes "prontos" sem entendê-los; preferir código que a equipe consegue explicar e reescrever.
- Termos de uso das ferramentas geralmente atribuem o output ao usuário, mas isso não impede reivindicações de terceiros.
- **Transparência acadêmica:** declaramos no template de PR (checkbox "IA assistiu este PR") e neste relatório onde a IA foi usada.

### 4.4 Centralidade da homologação e revisão humana no SDD
No Spec-Driven Development a **especificação é o contrato**; a IA é apenas um executor. Isso impõe três pontos de controle humanos que não podem ser delegados:
1. **Aprovar a SPEC:** só humanos (equipe + cliente) decidem regras de negócio. A IA pode sugerir, nunca decidir (ver RE-02, decisão sobre teto de multa).
2. **Revisar o código:** todo PR precisa de aprovação de alguém que não o autor — inclusive quando o "autor" foi uma IA. O revisor deve conseguir explicar cada linha.
3. **Homologar o resultado:** testes verdes provam que o código cumpre os testes, não que os testes cumprem a necessidade real. A validação final é humana.

Responsabilidade não é transferível: se um bug gerado por IA causar cobrança indevida a um membro, a responsabilidade é da equipe que fez o merge.

## 5. Conclusão
[PREENCHER — 1 parágrafo com a opinião do grupo: em quais tarefas a IA valeu a pena, em quais atrapalhou, e como vocês usariam em um próximo projeto.]
