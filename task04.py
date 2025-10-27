from functools import wraps
from typing import Callable
from collections import defaultdict

# handler decorator
def input_error(func: Callable) -> Callable:
    """
    Decorator to handle typical errors caused by wrong user input.
    """
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, IndexError):
            return "Wrong argument(-s) provided. Try again."
        except KeyError:
            return "No such contact found."
    return inner

# handlers
@input_error
def parse_input(user_input: str) -> tuple[str,list[str]]:
    """
    Parses user input into command and arguments.
    """
    cmd, *args = user_input.strip().split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args: list[str], contacts: dict[str, str]) -> str:
    """
    Adds new entry to contacts dictionary. 
    Returns a warning if contact with such name already exists, but anyway rewrites it.
    "args" should contain 2 values.
    """
    warning = ""
    name, phone = args
    if name in contacts:
        warning = f"WARNING: rewriting existing contact '{name}'=>'{contacts[name]}'!\n"
    contacts[name] = phone
    return warning + "Contact added."

@input_error
def change_contact(args: list[str], contacts: dict[str,str]) -> str:
    """
    Updates existing contact with new phone value.
    Returns an error message if contact with given name does not exist.
    "args" should contain 2 values.
    """
    name, phone = args
    if name not in contacts:
        return f"ERROR: contact '{name}' does not exist!"
    else:
        contacts[name] = phone
        return "Contact updated."

@input_error
def show_phone(args: list[str], contacts: dict[str: str]) -> str:
    """
    Returns phone for given name.
    Returns an error message if contact with such name is absent.
    """
    name = args[0]
    return contacts[name]

def show_all(_, contacts: dict[str, str]) -> str:
    """
    Outputs all the contents of in-memory database of contacts.
    """
    result = []
    for name, phone in contacts.items():
        result.append(f"{name}: {phone}")
    return "\n".join(result)


def main():
    # storage for contacts
    contacts = {}

    # command handlers

    def default_handler():
        def inner(*args, **kwargs):
            return "Invalid command."
        return inner

    # all handlers should take 2 arguments - args list and contacts dictionary
    handlers = defaultdict(default_handler)
    handlers["hello"] = lambda x,y: "How can I help you?"
    handlers["close"] = lambda x,y: "Good bye!"
    handlers["exit"] = lambda x,y: "Good bye!"
    handlers["add"] = add_contact
    handlers["change"] = change_contact
    handlers["phone"] = show_phone
    handlers["all"] = show_all

    print("Welcome to the assistant bot!")

    # main loop
    command = ""
    while command not in ["close", "exit"]:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)
        print(handlers[command](args, contacts))

if __name__ == "__main__":
    main()
