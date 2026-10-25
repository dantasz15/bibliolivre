# Roteiro da Demonstração Funcional — 3 a 5 minutos

**Status:** roteiro preparado. A gravação e o envio para YouTube, Drive, Loom ou SharePoint ainda precisam ser feitos pelo estudante/equipe. Este arquivo não representa um vídeo gravado nem contém link fictício.

| Tempo | O que narrar | O que mostrar |
|---|---|---|
| 0:00–0:30 | Apresentar o problema: bibliotecas comunitárias controlam empréstimos manualmente e precisam de uma ferramenta local, sem servidor. | README e objetivo do BiblioLivre. |
| 0:30–1:00 | Explicar a arquitetura: CLI, serviços, repositório SQLite e especificação com requisitos rastreáveis. | `docs/SPEC.md` seção As-Built e diagrama do README. |
| 1:00–2:10 | Executar o fluxo: cadastrar livro e membro, emprestar, verificar disponibilidade, renovar e devolver. | Terminal com `make demo` ou comandos do README. Usar apenas dados fictícios. |
| 2:10–2:45 | Mostrar regras de negócio e privacidade, incluindo anonimização do membro e histórico preservado. | `docs/SPEC.md`, comando `membro-anonimizar` e teste da colisão do e-mail sentinela. |
| 2:45–3:35 | Executar a suíte e explicar o que a evidência mede. | `make coverage`; mostrar total de testes e relatório de cobertura. Esclarecer que cobertura não prova ausência de bugs. |
| 3:35–4:15 | Apresentar a versão e os limites da governança: release na `main`, CI, aprovação humana e ausência de revisão entre pares até existir aprovação real. | PR da release e status do GitHub Actions, após publicados. |
| 4:15–4:30 | Resumir um aprendizado: a auditoria detectou uma colisão de unicidade não coberta; foi corrigida e ganhou teste de regressão. | Teste `test_colisao_de_email_sentinela_nao_impede_anonimizacao`. |

## Antes de gravar

1. Atualizar o código local com a release revisada.
2. Criar um banco de demonstração descartável e usar somente nomes/e-mails fictícios.
3. Confirmar que a pipeline e o link de release exibidos correspondem à versão entregue.
4. Gravar entre 3 e 5 minutos, sem expor RA em terminal, segredos, dados pessoais reais ou abas privadas.
5. Publicar o vídeo e inserir o link verificável no PDF de submissão final.

## Perguntas prováveis

- **Por que CLI e SQLite?** O escopo foi pensado para bibliotecas pequenas, uso local e operação offline; uma interface web e múltiplas bibliotecas ficaram fora do escopo.
- **Como a aplicação trata multas?** R$ 0,50 por dia de atraso, com teto de R$ 20,00 por empréstimo; valores são armazenados em centavos.
- **O que acontece com concorrência?** A operação de empréstimo usa `BEGIN IMMEDIATE`; há teste com oito conexões independentes disputando um exemplar. Isso não comprova suporte em filesystem de rede.
- **100% de cobertura garante ausência de erros?** Não; é a proporção de linhas executadas na suíte, não prova que todos os requisitos e casos de uso estão corretos.
- **Quem homologa uma alteração?** Testes e CI são evidências automatizadas; a aprovação independente de uma pessoa real continua sendo necessária para integrar a release na `main`.