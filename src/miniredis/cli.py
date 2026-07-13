"""Interactive MiniRedis CLI.

Run:
  python -m miniredis.cli
  # or after install: miniredis
"""

from __future__ import annotations

import sys

from miniredis.commands import CommandError, dispatch, tokenize
from miniredis.store import Store


BANNER = """MiniRedis v0.1 — naive in-memory store
Type HELP for commands, EXIT to quit.
"""


def run_repl(store: Store | None = None) -> None:
    store = store or Store()
    print(BANNER, end="")
    while True:
        try:
            line = input("miniredis> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye.")
            return

        if not line:
            continue

        upper = line.upper()
        if upper in {"EXIT", "QUIT"}:
            print("Bye.")
            return

        try:
            parts = tokenize(line)
            result = dispatch(store, parts)
            if result != "":
                print(result)
        except CommandError as exc:
            print(str(exc))
        except TypeError as exc:
            print(f"ERR {exc}")


def main() -> None:
    run_repl()


if __name__ == "__main__":
    main()
    sys.exit(0)
