import console as dc


@dc.ConsoleCommand
def hello():
    """Greet the world."""
    print("Hello World")


@dc.ConsoleCommand(name="greet", aliases=["hi"])
def greet_person(person: str):
    """Greet a person."""
    print(f"Hello {person}!")


def main():
    dc.get_input()


if __name__ == "__main__":
    main()
