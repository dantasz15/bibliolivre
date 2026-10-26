# Encerramento da Entrega 3 — Entrega Final

Este guia registra o estado de encerramento do BiblioLivre e separa validações automáticas das etapas que dependem de demonstração humana.

## 1. Verificação técnica

A release foi validada com `make lint`, cobertura e harness Docker. A matriz de CI executou os testes em Python 3.10, 3.11 e 3.12; CodeQL também concluiu com sucesso. A evidência local e os links oficiais estão em [`TESTES.md`](TESTES.md). As demonstrações devem usar apenas dados fictícios.

## 2. Pull Request e governança

O PR #9, da branch `release/1.0.0` para `main`, foi revisado pelo próprio autor e integrado em 26/10/2026. Como o projeto é individual, o autor autorizou reduzir a zero o número de aprovações obrigatórias; a regra de Pull Request em `main` foi mantida. Não houve aprovação independente registrada. Os checks verdes demonstram validação automatizada, não revisão por pares.

## 3. Release versionada

A branch padrão do repositório é `main`. O PR #9 foi integrado no commit `6df47b8453967c3326b9dba40e780477a8452077`; a tag `v1.0.0` e a Release oficial foram publicadas apontando para esse commit. Os workflows de CI e CodeQL também passaram no commit integrado. Na verificação posterior, não havia PR aberto.

- [Release oficial BiblioLivre 1.0.0](https://github.com/dantasz15/bibliolivre/releases/tag/v1.0.0)
- [Pull Request #9 integrado](https://github.com/dantasz15/bibliolivre/pull/9)

## 4. Vídeo e PDF

O roteiro para uma demonstração funcional de 3–5 minutos está em [`ROTEIRO_APRESENTACAO.md`](ROTEIRO_APRESENTACAO.md). A gravação e publicação do vídeo permanecem pendentes até haver arquivo e URL verificável; este guia não substitui a gravação. Quando o link estiver disponível, atualize o PDF de submissão e este documento, usando dados fictícios e sem expor RA, credenciais ou dados pessoais reais.

O PDF acadêmico deve informar nome e RA somente na cópia destinada à instituição; evite publicar o RA no repositório público. Inclua os links da release, dos resultados de teste/CI e, quando disponível, do vídeo, além das limitações técnicas relevantes.
