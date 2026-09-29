# ADR-006 — Transações explícitas com `BEGIN IMMEDIATE`

**Status:** Aceita · **Data:** [PREENCHER]

## Contexto
O empréstimo faz *verificar disponibilidade → gravar*. Com o modo padrão do `sqlite3`, a transação só começa na primeira escrita; dois processos (ex.: dois computadores com a mesma pasta compartilhada) podem ler "1 disponível" ao mesmo tempo e ambos gravarem (ERR-06).

## Decisão
Conexão com `isolation_level=None` e um gerenciador `Repositorio.transacao()` que executa `BEGIN IMMEDIATE`, obtendo o lock de escrita **antes** das leituras de validação. Todas as operações de escrita do serviço rodam dentro dele. Transações aninhadas reaproveitam a externa.

## Alternativas
- **Restrição no banco (trigger contando empréstimos ativos):** garante o limite, mas espalha regra de negócio no SQL, dificultando teste e leitura.
- **Lock em arquivo no Python:** não funciona entre máquinas diferentes.
- **`BEGIN EXCLUSIVE`:** bloquearia também leitores sem necessidade.

## Consequências
+ Verificação e gravação indivisíveis; rollback automático quando uma regra falha no meio.
+ Teste com 8 threads e conexões independentes prova que só 1 empréstimo é criado.
− Escritas simultâneas esperam em fila (timeout de 10 s), aceitável para o volume de uma biblioteca comunitária.
