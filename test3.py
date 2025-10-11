import os
import subprocess
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory

history = InMemoryHistory()
session = PromptSession(history=history)

# Your dictionary of custom commands (simplified example)
custom_commands = {
    'myfunc': lambda: print("Custom function called!"),
    'thefunc2': lambda: print("Custom function 2 called!"),
    # Add more python functions here...
}

current_dir = os.getcwd()

while True:
    try:
        # Get input with prompt-toolkit, including history support
        text = session.prompt(f'{current_dir}> ')

        if not text.strip():
            continue

        parts = text.strip().split()
        cmd = parts[0]
        args = parts[1:]

        # Check if it's a custom function
        if cmd in custom_commands:
            custom_commands[cmd](*args)

        # Support native 'cd' command natively for directory tracking
        elif cmd == 'cd':
            if args:
                try:
                    os.chdir(args[0])
                    current_dir = os.getcwd()
                except FileNotFoundError:
                    print(f"cd: no such file or directory: {args[0]}")
            else:
                # Default to home directory
                home = os.path.expanduser("~")
                os.chdir(home)
                current_dir = home

        else:
            # Run as regular shell command in the tracked directory
            # Using shell=True to handle complex commands (caution in untrusted input)
            subprocess.run(text, shell=True, cwd=current_dir)

    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("\nKeyboardInterrupt")
    except EOFError:
        # Exit on Ctrl+D
        print("Exiting...")
        break
