# Ordem de implementação

Ordem pensada para **aula ao vivo** e para PRs pequenos no CV: cada passo adiciona um conceito e um teste legível.

## Já entregue (base da aula)

1. **Store + SET/GET** — modelo mental “chave → valor”.
2. **Dispatcher + erros de arity** — contrato de comando.
3. **CLI REPL** — demo em 30 segundos.
4. **DEL / EXISTS / DBSIZE / FLUSHDB** — mutação e introspecção.
5. **KEYS** — first contact com O(N) e anti-pattern de produção.
6. **EXPIRE/TTL lazy** — tempo sem background thread (ainda).

## Próximos (sugeridos na aula)

| Ordem | Entrega | Por quê nesta ordem | Prompt âncora pro modelo |
|-------|---------|---------------------|---------------------------|
| 7 | Listas (`LPUSH`…`LRANGE`) | segundo tipo sem sair de memória | “como Redis representa listas vs nosso `list`?” |
| 8 | `WRONGTYPE` em todos os caminhos | disciplina de tipo | “desenhe o type tag no Store” |
| 9 | Hashes | nested map, casos de cache de objeto | “quando o Redis muda encoding?” |
| 10 | Sets | membership e cardinalidade | “intset vs hashtable” |
| 11 | `SCAN` em cima de KEYS | mitiga o O(N) que já mostramos | “cursor opaco: desenhe o estado” |
| 12 | Snapshot JSON (`SAVE`/`LOAD`) | accountability de dados | “RDB vs nosso JSON: trade-offs” |
| 13 | AOF toy | replay / recovery story | “fsync always vs everysec” |
| 14 | Pub/Sub | I/O mental model sem TCP ainda | “fan-out: mermaid do publish” |
| 15 | TCP + RESP | deixa de ser só CLI | “event loop single-threaded do Redis” |
| 16 | Eviction LRU naive | pressão de memória | “approximate LRU: por quê aproximar?” |
| 17 | Sorted sets | estrutura “difícil” de CV | “skip list vs tree: por quê Redis escolheu?” |
| 18 | MULTI/EXEC | atomicidade | “WATCH e lost update” |

## Regra de ouro na aula

```text
explicar → diagrama → complexidade → teste falhando → patch mínimo → pytest verde → decision note
```

Não pule o diagrama. Recrutador não vê o chat; vê o PR e o `DECISIONS.md`.
