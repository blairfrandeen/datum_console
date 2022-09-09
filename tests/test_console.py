import sys

import pytest

import datum_console.console as dc


def console_input_test(command: str, quit_command: str = "q"):
    """Fixture for testing command line inputs to console.
    Arguments:
        command:        The command to send to the console
        quit_command:   The command to send immediately after
                        To cause the console to quit.
    """
    yield command
    yield "q"


@dc.ConsoleCommand
def simple_function():
    print("A simple function has been executed.")


alias_tests = ["af", "a", "alias_func"]


@dc.ConsoleCommand(aliases=alias_tests)
def aliased_function():
    print("A function has been called using an alias")


@pytest.mark.parametrize("alias", alias_tests)
def test_aliased_function(monkeypatch, capsys, alias):
    input_tester = console_input_test(alias)
    monkeypatch.setattr("builtins.input", lambda _: next(input_tester))
    with pytest.raises(SystemExit):
        dc.get_input()
    captured = capsys.readouterr()
    assert "A function has been called using an alias" in captured.out


def test_simple_function(monkeypatch, capsys):
    input_tester = console_input_test("simple_function")
    monkeypatch.setattr("builtins.input", lambda _: next(input_tester))
    with pytest.raises(SystemExit):
        dc.get_input()
    captured = capsys.readouterr()
    assert "A simple function has been executed." in captured.out
