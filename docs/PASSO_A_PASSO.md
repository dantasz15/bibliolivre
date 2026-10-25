# Encerramento da Entrega 3

Este guia distingue validações locais das etapas que dependem do GitHub e da gravação pelo estudante.

## 1. Verificação local

No clone do projeto, crie ambiente virtual e instale `.[dev]`. Execute `make lint` e `make coverage`; se houver Docker, execute `docker compose run --build --rm test` e construa a imagem runtime. Registre versões, commit e resultados. Não use dados pessoais reais na demonstração.

## 2. Pull Request e revisão humana

A branch `main` exige Pull Request e uma aprovação independente. Envie a branch `release/1.0.0` para revisão; aguarde CI/CodeQL e a aprovação de uma pessoa real. O autor não deve aprovar o próprio PR. Não altere a proteção nem fabrique comentários para contornar esse requisito.

## 3. Release versionada

Depois que a aprovação e os checks forem concluídos, incorpore o PR em `main`, confirme o commit final, crie a tag `v1.0.0` e publique a Release com notas correspondentes ao `CHANGELOG.md`. Confirme que a página da tag/release aponta para o commit incorporado e que não ficou PR de release aberto. Atualize README, governança e PDF com URLs reais.

## 4. Vídeo e PDF

Grave uma demonstração de 3–5 minutos usando o roteiro em `docs/ROTEIRO_APRESENTACAO.md`. Publique o arquivo em um serviço autorizado, teste que o link funciona e inclua-o no PDF. Até a gravação existir, não apresente este roteiro como vídeo entregue nem invente URL.

O PDF acadêmico deve informar nome e RA somente na cópia destinada à instituição; evite publicar o RA no repositório público. Inclua link da release, log de testes/cobertura, resultado de CI, link do vídeo e limitações relevantes.