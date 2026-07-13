"""Command dispatcher — maps Redis-like verbs to Store methods."""

from __future__ import annotations

from miniredis.store import Store


class CommandError(Exception):
    """Invalid arity, unknown command, or bad argument."""


def dispatch(store: Store, parts: list[str]) -> str:
    if not parts:
        return ""

    cmd = parts[0].upper()
    args = parts[1:]

    if cmd == "SET":
        if len(args) != 2:
            raise CommandError("ERR wrong number of arguments for 'set' command")
        return store.set(args[0], args[1])

    if cmd == "GET":
        if len(args) != 1:
            raise CommandError("ERR wrong number of arguments for 'get' command")
        value = store.get(args[0])
        return "(nil)" if value is None else value

    if cmd == "DEL":
        if len(args) < 1:
            raise CommandError("ERR wrong number of arguments for 'del' command")
        return str(store.delete(*args))

    if cmd == "EXISTS":
        if len(args) < 1:
            raise CommandError("ERR wrong number of arguments for 'exists' command")
        return str(store.exists(*args))

    if cmd == "KEYS":
        pattern = args[0] if args else "*"
        if len(args) > 1:
            raise CommandError("ERR wrong number of arguments for 'keys' command")
        found = store.keys(pattern)
        if not found:
            return "(empty list)"
        return "\n".join(f"{i + 1}) {k}" for i, k in enumerate(found))

    if cmd == "EXPIRE":
        if len(args) != 2:
            raise CommandError("ERR wrong number of arguments for 'expire' command")
        try:
            seconds = int(args[1])
        except ValueError as exc:
            raise CommandError("ERR value is not an integer or out of range") from exc
        return str(store.expire(args[0], seconds))

    if cmd == "TTL":
        if len(args) != 1:
            raise CommandError("ERR wrong number of arguments for 'ttl' command")
        return str(store.ttl(args[0]))

    if cmd == "DBSIZE":
        if args:
            raise CommandError("ERR wrong number of arguments for 'dbsize' command")
        return str(store.dbsize())

    if cmd == "FLUSHDB":
        if args:
            raise CommandError("ERR wrong number of arguments for 'flushdb' command")
        return store.flushdb()

    if cmd == "PING":
        return "PONG"

    if cmd == "HELP":
        return _help_text()

    raise CommandError(f"ERR unknown command '{parts[0]}'")


def _help_text() -> str:
    return """Supported commands (naive MiniRedis):
  SET key value
  GET key
  DEL key [key ...]
  EXISTS key [key ...]
  KEYS [pattern]
  EXPIRE key seconds
  TTL key
  DBSIZE
  FLUSHDB
  PING
  HELP
  EXIT / QUIT"""


def tokenize(line: str) -> list[str]:
    """Split a CLI line into tokens. Quotes keep spaces inside a value."""
    tokens: list[str] = []
    current: list[str] = []
    in_quotes = False
    i = 0
    while i < len(line):
        ch = line[i]
        if ch == '"':
            in_quotes = not in_quotes
        elif ch.isspace() and not in_quotes:
            if current:
                tokens.append("".join(current))
                current = []
        else:
            current.append(ch)
        i += 1
    if current:
        tokens.append("".join(current))
    if in_quotes:
        raise CommandError("ERR unmatched quote")
    return tokens
