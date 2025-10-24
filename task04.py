def parse_input(user_input: str) -> tuple[str,list[str]]:
    """
    Parses user input into command and arguments.
    """
    cmd, *args = user_input.strip().split()
    cmd = cmd.strip().lower()
    return cmd, *args

def add_contact(args: list[str], contacts: dict[str, str]) -> str:
    """
    Adds new entry to contacts dictionary. 
    Returns a warning if contact with such name already exists, but anyway rewrites it.
    "args" should contain 2 values, it is guaranteed by caller.
    """
    warning = ""
    name, phone = args
    if name in contacts:
        warning = f"WARNING: rewriting existing contact '{name}'=>'{contacts[name]}'!\n"
    contacts[name] = phone
    return warning + "Contact added."

def change_contact(args: list[str], contacts: dict[str,str]) -> str:
    """
    Updates existing contact with new phone value.
    Returns an error message if contact with given name does not exist.
    "args" should contain 2 values, it is guaranteed by caller.
    """
    name, phone = args
    if name not in contacts:
        return f"ERROR: contact '{name}' does not exist!"
    else:
        contacts[name] = phone
        return "Contact updated."

def show_phone(name: str, contacts: dict[str: str]) -> str:
    """
    Returns phone for given name.
    Returns an error message if contact with such name is absent.
    """
    if name not in contacts:
        return f"ERROR: contact '{name}' does not exist!"
    else:
        return contacts[name]

def show_all(contacts: dict[str, str]) -> str:
    """
    Outputs all the contents of in-memory database of contacts.
    """
    result = []
    for name, phone in contacts.items():
        result.append(f"{name}: {phone}")
    return "\n".join(result)

def main():
    contacts = {}
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"] and len(args) == 0:
            print("Good bye!")
            break
        elif command == "hello" and len(args) == 0:
            print("How can I help you?")
        elif command == "add" and len(args) == 2:
            print(add_contact(args, contacts))
        elif command == "change" and len(args) == 2:
            print(change_contact(args, contacts))
        elif command == "phone" and len(args) == 1:
            print(show_phone(args[0], contacts))
        elif command == "all" and len(args) == 0:
            print(show_all(contacts))
        else:
            # if command is unknown or number of arguments is wrong
            print("Invalid command.")

if __name__ == "__main__":
    main()