#!/usr/bin/env sh
# Executa a suíte e salva o log com data/ambiente em docs/evidencias/
set -e
cd "$(dirname "$0")/.."
mkdir -p docs/evidencias
LOG="docs/evidencias/test-log-$(date +%Y%m%d-%H%M%S).txt"
{
  echo "== BiblioLivre - execução do test harness =="
  echo "Data: $(date)"
  echo "Python: $(python3 --version 2>&1)"
  echo "SO: $(uname -a)"
  echo "Commit: $(git rev-parse --short HEAD 2>/dev/null || echo 'n/a')"
  echo
  python3 -m unittest discover -s tests -t . -v 2>&1
} | tee "$LOG"
echo "Log salvo em $LOG"
