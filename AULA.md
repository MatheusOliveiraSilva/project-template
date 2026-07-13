# Script da aula — projetos pessoais que o recruiter nota (via MiniRedis)

**Duração sugerida:** 90–120 min  
**Repo:** `project-template` (este)  
**Tese:** recruiter não lê seu chat com a IA — lê evidência: README que roda, roadmap, decisões, commits pequenos, testes legíveis.

---

## 0. Antes da aula (você, 15–20 min)

- [ ] Clone fresco numa pasta limpa; siga o README do zero (valida o “roda local”).
- [ ] `pip install -e ".[dev]" && pytest -v` → tudo verde.
- [ ] Abra o Cursor **neste repo**; confirme que a skill `.cursor/skills/teach-as-you-build/` aparece.
- [ ] Tenha 2–3 prompts prontos (seção Prompt bank).
- [ ] Decida a feature ao vivo do dia (default: **listas LPUSH/LPOP/LRANGE**).
- [ ] Abra `docs/ROADMAP.md` e `docs/DECISIONS.md` numa aba.

---

## 1. Abertura (10 min) — por que este formato de projeto

Fale pouco de Redis; fale do **pacote de sinal**:

| Sinal | Onde está neste repo |
|-------|----------------------|
| Accountability | issues/PRs por feature do roadmap; testes |
| Planejamento | `ROADMAP.md` + `IMPLEMENTATION_ORDER.md` |
| Clean code | módulos pequenos: store / commands / cli |
| Doc | `DECISIONS.md` (ADR leve) |
| README que roda | seção “Rodar local” |
| Roadmap | tabela feature × aprendizado |
| Decisões | naive vs Redis real |

**Frase âncora:** “IA acelera o código; o que diferencia no CV é o sistema em volta do código.”

Mostre o clone → venv → `miniredis` → `SET`/`GET` ao vivo (2 min).

---

## 2. Tour do MVP (15 min)

1. `store.py` — dict + expires lazy.  
2. `commands.py` — dispatcher.  
3. `test_commands.py` — teste = sessão.  
4. Pergunte à turma: “por que KEYS é perigoso?” → abra o código O(N).

**Demo com o agente (opcional, 3 min):**

```text
Usando teach-as-you-build: sem escrever código novo, explique KEYS neste repo.
Mermaid do fluxo + tabela de complexidade vs Redis SCAN.
```

Você narra o que o modelo acertou/errou. Isso ensina **como estudar com o repo**.

---

## 3. Bloco principal — iterar uma feature ao vivo (40–50 min)

### Setup do chat

```text
Estamos na aula. Use teach-as-you-build.
Feature: roadmap #4 — listas LPUSH, RPUSH, LPOP, RPOP, LRANGE.
Regras: explicar → mermaid → complexidade → teste → patch mínimo.
Depois de cada passo, pare e me diga a pergunta que eu faço pra turma.
```

### Ritmo sugerido

| Min | Você faz | Turma vê |
|-----|----------|----------|
| 0–5 | Cola o prompt; deixa gerar diagramas | modelo mental |
| 5–10 | Pausa: “O valor deixou de ser só string — e agora?” | WRONGTYPE |
| 10–20 | Pede o teste falhando primeiro | TDD leve |
| 20–35 | Aplica patch; roda `pytest` | feedback loop |
| 35–45 | “Como seria no Redis de verdade?” | quicklist / listpack |
| 45–50 | Escreve ADR-005 juntos no `DECISIONS.md` | accountability |

### Perguntas boas pra turma (use 3–4)

1. Se `GET` numa key que é lista — o que deve acontecer?  
2. `LRANGE` com índices negativos: copiamos Redis ou simplificamos? (decisão de produto)  
3. Complexidade de `LPOP` no nosso `list` vs na quicklist?  
4. Isso entra no CV como “clonei Redis” ou como “estudei estruturas com trade-offs documentados”?  

---

## 4. Meta-aula — como estudar sozinho depois (15 min)

Mostre o loop que eles repetem em casa:

```text
escolher linha do ROADMAP
  → issue com critério de aceite
  → prompt teach-as-you-build
  → PR pequeno + teste
  → ADR se mudou trade-off
  → atualizar status no ROADMAP
```

**Anti-padrão a nomear:** 40 commits “wip” sem README; ou um monólito gerado sem decisões.

Diga explicitamente: a opção 2 da votação (projetos educativos) é o **mesmo repo** — só muda a profundidade das perguntas ao modelo.

---

## 5. Fechamento (10 min)

- Recap dos 7 sinais do recruiter.  
- Próximo ciclo: não é mais “aula de IA” — apontar o que vem.  
- Homework opcional: implementar **hashes** ou **SCAN** em fork próprio; abrir PR descrevendo naive vs real.  
- Link do repo + pedir estrela/fork.

---

## Prompt bank

### A — Explorar sem codear

```text
teach-as-you-build: explique EXPIRE/TTL lazy neste repo.
Mermaid sequence do GET com chave expirada.
O que o Redis faz a mais (active expire)? Sem patch.
```

### B — Feature ao vivo

```text
teach-as-you-build: implemente LPUSH/RPUSH/LPOP/RPOP/LRANGE.
Testes no estilo test_commands.py.
Pare antes do código até eu aprovar os diagramas.
```

### C — Empurrão de CV

```text
Com base neste repo, redija um parágrafo de README “Why this project”
para LinkedIn/CV: foco em planejamento, trade-offs e testes — sem marketing vazio.
```

### D — Comparação dura

```text
teach-as-you-build: se KEYS tiver 5 milhões de chaves no nosso Store, o que acontece?
Desenhe SCAN como mitigação (só desenho + esqueleto de API, sem implementar tudo).
```

---

## Plano B (se a rede/API falhar)

1. Whiteboard: dict + expires.  
2. Escrever `LPUSH` na mão em 15 linhas.  
3. Rodar pytest local.  
4. Discutir ADR no `DECISIONS.md` offline.

---

## Checklist de sucesso da aula

- [ ] Alguém da turma rodou o CLI com sucesso.  
- [ ] Pelo menos um mermaid apareceu na tela.  
- [ ] Uma comparação O(N) vs Redis real foi dita em voz alta.  
- [ ] Um ADR novo (mesmo rascunho) foi commitado ou mostrado.  
- [ ] Homework + link do repo claros.
