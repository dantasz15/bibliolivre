# Roteiro da Apresentação / Vídeo (≈ 8 min)

| Tempo | Quem | Conteúdo | O que mostrar na tela |
|---|---|---|---|
| 0:00–1:00 | Membro 1 | Problema: biblioteca comunitária no caderno; público sem internet e sem TI | Slide com o problema |
| 1:00–2:00 | Membro 1 | SDD: SPEC como fonte da verdade, IDs RN-xx rastreados até os testes | `docs/SPEC.md` + matriz em `docs/TESTES.md` |
| 2:00–3:30 | Membro 2 | Demo ao vivo: cadastrar, emprestar, atrasar, multa, pagar | `make demo` ou comandos do README |
| 3:30–4:30 | Membro 3 | Arquitetura e 2 ADRs mais importantes (006 concorrência, 005 centavos) | Diagrama do README |
| 4:30–5:30 | Membro 3 | Testes: 46 testes, 100% de cobertura, propriedade, concorrência; CI verde | Aba Actions |
| 5:30–6:30 | Membro 4 | Loop de re-especificação: RE-03 (brecha de bloqueio) e RE-05 (ética virou requisito) | `docs/ERROS_E_RE_ESPECIFICACAO.md` |
| 6:30–7:30 | Membro 4 | IA: onde ajudou, onde errou, por que a revisão humana é obrigatória | `docs/RELATORIO_IA.md` |
| 7:30–8:00 | Todos | Aprendizados e o que fariam diferente | — |

## Perguntas prováveis na defesa (e respostas curtas)

**Por que não um sistema web?**
O público-alvo não tem servidor nem internet confiável (RNF-02). A arquitetura em camadas permite trocar a CLI por uma interface web sem mexer nas regras (ADR-001, ADR-003).

**Por que SQLite e não PostgreSQL?**
Zero instalação, backup copiando um arquivo. O limite é o acesso multiusuário em rede, fora do escopo (ADR-002).

**Como vocês garantem que dois voluntários não emprestam o mesmo último livro?**
Com `BEGIN IMMEDIATE`, que pega o lock de escrita antes de verificar a disponibilidade (ADR-006). O teste dispara 8 conexões ao mesmo tempo e confere que só uma vence.

**Por que centavos e não float?**
`0.1 + 0.2 != 0.3` em ponto flutuante. Tivemos esse bug (ERR-02) e a correção virou o ADR-005.

**O que é um teste de propriedade?**
Em vez de testar um exemplo, gera milhares de operações aleatórias e verifica regras que sempre devem valer, como disponibilidade nunca negativa. A semente é fixa para a falha poder ser reproduzida (ADR-007).

**100% de cobertura significa que não há bugs?**
Não. Significa que toda linha foi executada, não que todo comportamento foi verificado. Por isso complementamos com testes de borda, de propriedade e de concorrência.

**Qual foi a maior contribuição da IA? E o maior erro?**
[Responder com a experiência real do grupo.] Sugestão de estrutura: ajudou no boilerplate e em sugerir casos de teste; não percebeu sozinha a corrida (ERR-06) nem a brecha de regra (RE-03).

**O código gerado por IA é de quem?**
A autoria é juridicamente incerta; a Lei 9.610/98 pressupõe autor humano. Mitigamos revisando e entendendo cada linha, e declarando o uso de IA em cada PR.

**Por que a revisão humana é obrigatória se os testes passam?**
Testes provam que o código cumpre os testes, não que os testes cumprem a necessidade. Quem decide a regra (ex.: teto da multa) é humano, e a responsabilidade pelo merge também.

**Mostre uma regra da SPEC no código e no teste.**
RN-07: `TETO_MULTA_CENTAVOS` em `services.py` → `test_calculo_multa_limites` (casos 40 e 41 dias) → `test_multa_monotona_e_limitada`.
