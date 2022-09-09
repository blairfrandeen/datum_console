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


alias_tests = ["af", "a", "alias_func"]


@dc.ConsoleCommand(aliases=alias_tests)
def aliased_function():
    """An Aliased Function"""
    print("A function has been called using an alias")


@dc.ConsoleCommand
def argument_function(arg):
    print(f"This is not an argument, it's a mere {arg}!")


@dc.ConsoleCommand
def kw_argument_function(isnt="argument", isamere="contradiction"):
    print(f"This is not an {isnt}, it's a mere {isamere}!")


@dc.ConsoleCommand
def simple_function():
    """A simple function"""
    print("A simple function has been executed.")


@dc.ConsoleCommand
def undocumented_function():
    pass


@dc.ConsoleCommand
def input_err_function():
    raise dc.InputError("Test Error")


@dc.ConsoleCommand(enabled=False)
def disabled_function():
    print("You shouldn't be seeing this")


def test_disabled_function(monkeypatch, capsys):
    input_tester = console_input_test(f"disabled_function")
    monkeypatch.setattr("builtins.input", lambda _: next(input_tester))
    with pytest.raises(SystemExit):
        dc.get_input()
    captured = capsys.readouterr()
    assert "Disabled" in captured.out
    assert "You shouldn't be seeing this" not in captured.out


@pytest.mark.parametrize("argument", ["conversation", "discussion", "contradiction"])
def test_argument_function(argument, monkeypatch, capsys):
    input_tester = console_input_test(f"argument_function {argument}")
    monkeypatch.setattr("builtins.input", lambda _: next(input_tester))
    with pytest.raises(SystemExit):
        dc.get_input()
    captured = capsys.readouterr()
    assert f"a mere {argument}!" in captured.out


@pytest.mark.xfail
@pytest.mark.parametrize(
    "isnt, isamere", [("dog", "cat"), (None, None), (None, "banana"), ("banana", None)]
)
def test_kw_argument_function(isnt, isamere, monkeypatch, capsys):
    input_str = "kw_argument_function"
    if isnt is not None:
        input_str += f" isnt={isnt}"
    if isamere is not None:
        input_str += f" isamere={isamere}"
    input_tester = console_input_test(input_str)
    monkeypatch.setattr("builtins.input", lambda _: next(input_tester))
    with pytest.raises(SystemExit):
        dc.get_input()
    captured = capsys.readouterr()
    if isnt is not None:
        assert f"is not an {isnt}, " in captured.out
    else:
        assert f"is not an argument" in captured.out
    if isamere is not None:
        assert f"it's a mere {isamere}!" in captured.out
    else:
        assert f"it's a mere contradiction!" in captured.out


@pytest.mark.parametrize("alias", alias_tests)
def test_aliased_function(monkeypatch, capsys, alias):
    input_tester = console_input_test(alias)
    monkeypatch.setattr("builtins.input", lambda _: next(input_tester))
    with pytest.raises(SystemExit):
        dc.get_input()
    captured = capsys.readouterr()
    assert "A function has been called using an alias" in captured.out


def test_help(monkeypatch):
    input_tester = console_input_test("help")
    monkeypatch.setattr("builtins.input", lambda _: next(input_tester))
    with pytest.raises(SystemExit):
        dc.get_input()


@pytest.mark.parametrize("quit_cmd", ["quit", "q"])
def test_quit(quit_cmd, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: quit_cmd)
    with pytest.raises(SystemExit):
        dc.get_input()


def test_simple_function(monkeypatch, capsys):
    input_tester = console_input_test("simple_function")
    monkeypatch.setattr("builtins.input", lambda _: next(input_tester))
    with pytest.raises(SystemExit):
        dc.get_input()
    captured = capsys.readouterr()
    assert "A simple function has been executed." in captured.out


def test_invalid_command(monkeypatch, capsys):
    input_tester = console_input_test("invalid_command")
    monkeypatch.setattr("builtins.input", lambda _: next(input_tester))
    with pytest.raises(SystemExit):
        dc.get_input()
    captured = capsys.readouterr()
    assert "Command not recognized. Type 'h' for help or 'q' to quit." in captured.out


def test_input_err_function(monkeypatch, capsys):
    input_tester = console_input_test("input_err_function")
    monkeypatch.setattr("builtins.input", lambda _: next(input_tester))
    with pytest.raises(SystemExit):
        dc.get_input()
    captured = capsys.readouterr()
    assert "Error:  Test Error" in captured.out
