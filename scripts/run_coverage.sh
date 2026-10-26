#!/usr/bin/env bash
# Executa testes com coverage.py, exige pelo menos 95% e salva evidências locais.
set -euo pipefail
cd "$(dirname "$0")/.."

if ! python3 -m coverage --version >/dev/null 2>&1; then
  echo "coverage.py não está instalado. Execute: python3 -m pip install -e '.[dev]'" >&2
  exit 2
fi

evidence_dir="${BIBLIO_EVIDENCE_DIR:-docs/evidencias}"
mkdir -p "$evidence_dir"
stamp="$(date -u +%Y%m%dT%H%M%SZ)"
log="$evidence_dir/coverage-${stamp}.txt"
xml="$evidence_dir/coverage-${stamp}.xml"
{
  echo "== BiblioLivre — testes e cobertura de linhas =="
  echo "Data UTC: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "Python: $(python3 --version 2>&1)"
  echo "coverage.py: $(python3 -m coverage --version)"
  echo "Branch: $(git branch --show-current 2>/dev/null || echo n/a)"
  echo "Commit de referência: $(git rev-parse HEAD 2>/dev/null || echo n/a)"
  echo "Estado de trabalho: $(if git diff --quiet && git diff --cached --quiet; then echo limpo; else echo contém alterações; fi)"
  echo
  python3 -m coverage erase
  python3 -m coverage run --source=bibliolivre --omit='bibliolivre/__main__.py' \
    -m unittest discover -s tests -t . -v
  echo
  python3 -m coverage report --show-missing --fail-under=95
} 2>&1 | tee "$log"
python3 -m coverage xml -o "$xml"
echo "Log: $log"
echo "XML: $xml"
