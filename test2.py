# IMPORTS
from prompt_toolkit.completion import NestedCompleter
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory  # or use FileHistory for disk p
from prompt_toolkit import prompt

# COMPLETER
completer = NestedCompleter.from_nested_dict({
    "show": {
        "version": None,
        "clock": None,
        "ip": {
            "interface": {"brief", "details"}
        }
    },
    "configure": {
        "terminal": None,
        "interface": {
            "ethernet": {"0/1", "0/2"},
            "loopback": {"0", "1"}
        }
    },
    "exit": None,
})

# SESSION INIT
history = InMemoryHistory()
session = PromptSession(history=history, completer=completer)


# CLI LOOP
text = ""
while text != "!!":
    text = session.prompt('YourCLI> ')
    print(f'You entered: {text}')
