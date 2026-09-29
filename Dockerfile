FROM python:3.14-slim AS base
WORKDIR /app
COPY bibliolivre/ bibliolivre/
ENV BIBLIO_DB=/dados/bibliolivre.db
RUN mkdir -p /dados && useradd -m app && chown app /dados
USER app

FROM base AS test
COPY tests/ tests/
RUN python -m unittest discover -s tests -t . -v

FROM base AS runtime
ENTRYPOINT ["python", "-m", "bibliolivre"]
CMD ["--help"]
