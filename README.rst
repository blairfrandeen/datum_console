Datum Console
======
This is a python library for creating interactive command line applications.

Basic Usage
----
Simply add the `@dc.ConsoleCommand` decorator to any function that you want to be accessible from within an interactive prompt. Run the `dc.get_input()` function to start the prompt.

The `help` and `quit` commands are automatically generated.

.. code-block:: python
    import datum_console.console as dc

    @dc.ConsoleCommand
    def hello():
        """Greet the world."""
        print("Hello World")

    dc.get_input()

.. code-block:: python
    >>> import datum_console.console as dc
    >>> @dc.ConsoleCommand
    ... def hello():
    ...     """Greet the world."""
    ...     print("Hello World")
    ...
    >>> dc.get_input()
    >>h
    Available commands:
      hello               Greet the world.
      help, h             Display this help message. Type help <command> for more detail.
      quit, q             Exit the console
    >>hello
    Hello World
    >>quit
