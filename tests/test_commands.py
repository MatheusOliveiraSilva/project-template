"""Readable command tests — each test is a tiny Redis session story."""

from __future__ import annotations

import time

import pytest

from miniredis.commands import CommandError, dispatch, tokenize
from miniredis.store import Store


def run(store: Store, line: str) -> str:
    return dispatch(store, tokenize(line))


def test_ping():
    assert run(Store(), "PING") == "PONG"


def test_set_get():
    s = Store()
    assert run(s, "SET name matheus") == "OK"
    assert run(s, "GET name") == "matheus"


def test_get_missing_key():
    assert run(Store(), "GET missing") == "(nil)"


def test_del_and_exists():
    s = Store()
    run(s, "SET a 1")
    run(s, "SET b 2")
    assert run(s, "EXISTS a b c") == "2"
    assert run(s, "DEL a") == "1"
    assert run(s, "EXISTS a") == "0"
    assert run(s, "GET a") == "(nil)"


def test_keys_all_and_pattern():
    s = Store()
    run(s, "SET user:1 alice")
    run(s, "SET user:2 bob")
    run(s, "SET session:9 xyz")
    assert run(s, "KEYS") == "1) user:1\n2) user:2\n3) session:9"
    assert run(s, "KEYS user:*") == "1) user:1\n2) user:2"


def test_expire_and_ttl():
    s = Store()
    run(s, "SET temp hello")
    assert run(s, "TTL temp") == "-1"
    assert run(s, "EXPIRE temp 2") == "1"
    ttl = int(run(s, "TTL temp"))
    assert 0 <= ttl <= 2


def test_expire_removes_key_after_deadline():
    s = Store()
    run(s, "SET temp hello")
    run(s, "EXPIRE temp 1")
    time.sleep(1.1)
    assert run(s, "GET temp") == "(nil)"
    assert run(s, "TTL temp") == "-2"


def test_dbsize_and_flushdb():
    s = Store()
    run(s, "SET a 1")
    run(s, "SET b 2")
    assert run(s, "DBSIZE") == "2"
    assert run(s, "FLUSHDB") == "OK"
    assert run(s, "DBSIZE") == "0"


def test_quoted_value_with_spaces():
    s = Store()
    assert run(s, 'SET msg "hello world"') == "OK"
    assert run(s, "GET msg") == "hello world"


def test_unknown_command():
    with pytest.raises(CommandError, match="unknown command"):
        run(Store(), "FOOBAR")


def test_wrong_arity():
    with pytest.raises(CommandError, match="wrong number"):
        run(Store(), "SET only_one_arg")
