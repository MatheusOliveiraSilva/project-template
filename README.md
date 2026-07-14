# MiniRedis — project template

Um Redis **ingênuo** (in-memory) em Python: CLI + testes legíveis.

Feito para a aula **como fazer projetos pessoais que o recruiter nota** — accountability, planejamento, clean code, docs, README que roda local, roadmap e decisões. Na aula a gente itera features ao vivo com AI e compara com o Redis de verdade (complexidade, estruturas, trade-offs).

> Não é um clone de produção. É um laboratório: implementação naive de propósito, para você melhorar com intenção.

---

## O que já existe (MVP)

| Comando | Comportamento |
|---------|----------------|
| `SET key value` | grava string |
| `GET key` | lê string ou `(nil)` |
| `DEL key ...` | remove chaves |
| `EXISTS key ...` | conta chaves vivas |
| `KEYS [pattern]` | lista chaves (`*` / `?`) — **O(N)** |
| `EXPIRE key seconds` | TTL lazy (checa no acesso) |
| `TTL key` | segundos restantes / `-1` / `-2` |
| `DBSIZE` / `FLUSHDB` / `PING` / `HELP` | utilitários |

---

## Rodar local

Requisitos: **Python 3.11+**

```bash
# clone
git clone https://github.com/MatheusOliveiraSilva/project-template.git
cd project-template

# venv + install editável (com pytest)
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# CLI interativa
miniredis
# ou: python -m miniredis.cli
```

Sessão de exemplo:

```text
miniredis> SET user:1 alice
OK
miniredis> GET user:1
alice
miniredis> KEYS user:*
1) user:1
miniredis> EXPIRE user:1 60
1
miniredis> TTL user:1
59
miniredis> EXIT
```

### Testes

```bash
pytest -v
```

Cada teste em `tests/test_commands.py` é uma mini-sessão Redis — leia como especificação viva.

---

## Estrutura

```text
src/miniredis/
  store.py      # dict + expires (naive)
  commands.py   # dispatcher SET/GET/...
  cli.py        # REPL
tests/
  test_commands.py
.cursor/skills/
  teach-as-you-build/   # skill didática para estudar com o agente
docs/
  ROADMAP.md            # features × o que você aprende
  IMPLEMENTATION_ORDER.md
  DECISIONS.md          # ADRs leves
AULA.md                 # script do instrutor
```

---

## Documentos da aula / CV

| Doc | Por quê importa pro recruiter |
|-----|-------------------------------|
| [docs/ROADMAP.md](docs/ROADMAP.md) | mostra que você planeja, não só code dump |
| [docs/IMPLEMENTATION_ORDER.md](docs/IMPLEMENTATION_ORDER.md) | ordem de entrega incremental |
| [docs/DECISIONS.md](docs/DECISIONS.md) | trade-offs conscientes (naive vs real Redis) |
| [AULA.md](AULA.md) | como rodar a aula e o que perguntar ao modelo |

---

## Estudar com AI neste repo

O arquivo [`AGENTS.md`](AGENTS.md) manda o agente **ensinar sem codear** até você pedir. Para implementação guiada, use a skill **teach-as-you-build**.

Prompt seed (só estudar):

```text
Não implemente. Explique KEYS neste repo vs SCAN no Redis real.
Mermaid do fluxo + tabela de complexidade. Termine com 1 pergunta pra eu pensar.
```

Prompt seed (quando quiser código):

```text
Agora pode implementar LPUSH/LPOP. Patch mínimo + teste no estilo test_commands.py.
```

---

## Licença

MIT — use, fork, melhore na aula e no CV.
