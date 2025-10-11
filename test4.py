import os
import subprocess
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.completion import NestedCompleter

# Sample commands dictionary with nested subcommands example
commands = {
    'openDevFolder': None, 
    'runServer': {'cmd': None}, 
    'scan': None,
    'scan:': {
        'os': None,
        'port': {
            'web',
            'native'
        }
    }
}
# commands = {
#     'openDevFolder': {'cmd': 'open ~/Documents/Dev'}, 
#     'runServer': {'cmd': 'x = find . -iname "main.py"\npython3 x\n'}, 
#     'scan': {'cmd': 'nmap $1', 'subcmd': {
#         'os': {'cmd': 'nmap -o $1'}, 
#         'port': {'cmd': 'nmap -sP $1', 'subcmd': {
#             'web': {'cmd': 'nmap -sP $1 -p 80, 443'}
#         }}
#     }}
# }


# Custom function implementations mapped by command name
def openDevFolder():
    print("Opening developer folder...")
    subprocess.run("open ~/Documents/Dev", shell=True)

def runServer():
    print("Running server script...")
    # Your actual command could be more complex
    subprocess.run('find . -iname "main.py"', shell=True)

# Map custom commands to Python functions
custom_commands = {
    "openDevFolder": openDevFolder,
    "runServer": runServer,
    # Add more custom Python command handlers here
}

# Prompt-toolkit completer for commands and nested subcommands
completer = NestedCompleter.from_nested_dict(commands)

def expand_path(path):
    # Expand ~ and environment variables
    return os.path.expandvars(os.path.expanduser(path))

def change_directory(path):
    try:
        target_path = expand_path(path) if path else os.path.expanduser('~')
        os.chdir(target_path)
        return os.getcwd()
    except FileNotFoundError:
        print(f"cd: no such file or directory: {path}")
        return None
    except NotADirectoryError:
        print(f"cd: not a directory: {path}")
        return None
    except PermissionError:
        print(f"cd: permission denied: {path}")
        return None

def main():
    history = InMemoryHistory()
    session = PromptSession(history=history, completer=completer)

    current_dir = os.getcwd()

    while True:
        try:
            prompt_str = f'{current_dir} > '
            text = session.prompt(prompt_str).strip()

            if not text:
                continue

            parts = text.split()
            cmd = parts[0]
            args = parts[1:]

            # Check if command is Python native custom command
            if cmd in custom_commands:
                custom_commands[cmd](*args)

            # Handle native 'cd' command with support for '~' and empty arg (go home)
            elif cmd == 'cd':
                new_dir = change_directory(args[0] if args else None)
                if new_dir:
                    current_dir = new_dir

            # Handle 'pwd' natively for accurate current directory
            elif cmd == 'pwd':
                print(current_dir)

            # Handle basic 'exit' or EOF to quit cleanly
            elif cmd in {'exit', 'quit'}:
                print("Exiting...")
                break

            else:
                # Run any other command in the current directory context
                subprocess.run(text, shell=True, cwd=current_dir)

        except KeyboardInterrupt:
            # Gracefully handle Ctrl+C - just go to next prompt
            print()
        except EOFError:
            # Exit on Ctrl+D
            print("Exiting...")
            break

if __name__ == "__main__":
    main()
