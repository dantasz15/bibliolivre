# Roteiro da Demonstração Funcional — Entrega Final

**Status:** demonstração final publicada como asset da release pública [`v1.0.0`](https://github.com/dantasz15/bibliolivre/releases/tag/v1.0.0). O vídeo tem 3min44s, resolução 1080p e narração em português brasileiro. A composição usa motion graphics; as telas de terminal exibem comandos e resultados executados na CLI real, em banco SQLite temporário e com dados fictícios. Não se trata de captura contínua da tela.

**[Assistir/baixar a demonstração funcional](https://github.com/dantasz15/bibliolivre/releases/download/v1.0.0/BiblioLivre_Demonstracao_Final.mp4)**

| Tempo | Conteúdo narrado e mostrado |
|---|---|
| 0:00–0:15 | Apresentação do BiblioLivre e seu objetivo para bibliotecas comunitárias. |
| 0:15–0:24 | Identificação acadêmica do projeto intermediário — Entrega Final de Bootcamp III. |
| 0:24–0:53 | Arquitetura em camadas, especificação, testes, opções Python/Docker e uso de dados fictícios. |
| 0:53–1:35 | Cadastro de livro e pessoa leitora; empréstimo, disponibilidade, renovação, consulta de atrasos, devolução e multa. |
| 1:35–2:04 | Anonimização, ressalva sobre LGPD e correção de colisão do e-mail sentinela com teste de regressão. |
| 2:04–2:35 | 47 testes em Python 3.10, 3.11 e 3.12, 100% de cobertura em 348 instruções, Ruff, Docker, CI e CodeQL; limites da métrica. |
| 2:35–3:05 | Release oficial, integração dos PRs e transparência sobre a revisão individual. |
| 3:05–3:28 | Escopo e limitações de implantação e uso do SQLite local. |
| 3:28–3:44 | Encerramento com os links do repositório e da release. |

## Proteção de dados e interpretação

A execução usa um arquivo `demo.sqlite3` temporário, a pessoa fictícia “Lia Martins” e um endereço reservado ao uso de testes (`example.test`). O vídeo não exibe o RA. Os resultados correspondem a comandos reais da aplicação, embora o layout seja uma composição gráfica, e não uma gravação contínua da interface. A anonimização demonstrada é uma funcionalidade; não constitui certificação de conformidade integral com a LGPD.

A demonstração registra o fluxo funcional e os principais resultados de homologação. A cobertura de 100% é a proporção de linhas exercitadas pela suíte, não uma prova de ausência de defeitos. CI e CodeQL não equivalem a revisão por pares. Por se tratar de trabalho individual, o próprio autor revisou a entrega, sem aprovação independente registrada.

## Perguntas prováveis

- **Por que CLI e SQLite?** O escopo foi pensado para bibliotecas pequenas, uso local e operação offline; uma interface web e múltiplas bibliotecas ficaram fora do escopo.
- **Como a aplicação trata multas?** R$ 0,50 por dia de atraso, com teto de R$ 20,00 por empréstimo; valores são armazenados em centavos.
- **O que acontece com concorrência?** A operação de empréstimo usa `BEGIN IMMEDIATE`; há teste com oito conexões independentes disputando um exemplar. Isso não comprova suporte em filesystem de rede.
- **100% de cobertura garante ausência de erros?** Não; é a proporção de linhas executadas na suíte, não prova que todos os requisitos e casos de uso estão corretos.
- **Quem homologou esta release?** O autor fez a revisão por se tratar de trabalho individual; não houve aprovação independente registrada. Testes e CI são evidências automatizadas e não equivalem a revisão por pares. A regra de `main` continua exigindo PR.
