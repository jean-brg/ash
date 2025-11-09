# ASH - AutoShell

## Philosophy
ASH is a lightweight CLI tool built by a developer, for developers. It aims to stay minimal  
by default, yet powerful when you need it — making complexity a choice, not a burden.

## Reserved Keywords
- YAML key `cmd` in the YAML file: Defines the shell code of a function
- YAML key prefix `$` in the YAML file: Defines the metadata of a function
- Command names prefix `ash-`: Reserved for ASH built-in functions
- File `ash.config.yaml`: Defines the main configuration and command registry
- File `ash-source.sh`: Reserved to source custom commands in current shell

## File Location
To mitigate issues, the `ash.py` and `ash.config.yaml` file should always stay in the same directory.   
As for where to put these files on your machine, these locations are suggested (but not required):
- Mac: `~/.config/ash/`
- Windows: `%APPDATA%\ash\`
- Linux: `~/.config/ash/` or `/usr/local/share/ash/`

## Installation
### 1. Clone the repository:
```shell
git clone https://github.com/jean-brg/ash.git
cd ash
```

### 2. Add ASH to your shell
Add the following function to your shell configuration file  
(~/.zshrc for Zsh, ~/.bashrc or ~/.bash_profile for Bash):
```
ash() {
    python3 /path/to/ash.py "$@"
}
```
Then restart your terminal or run:
```shell
source ~/.zshrc    # or ~/.bashrc
```

### 3. Optional: Copy the sample commands
```shell
cp ash.config.sample.yaml ash.config.yaml
```
You can now edit `ash.config.yaml` to add your own commands.

### 4. Optional: Set up `ash-source`
See below for detail

## Using ash-source
### What is ash-source
The `ash-source` command imports your ASH commands into the current shell to  
make them feel like native functions. This also means they won't have to be   
prefixed with `ash` to be called.

### How to use it
Due to Python’s process isolation, shell functions cannot persist automatically across sessions.   
Therefore, `ash-source` needs to be run once per shell session, or added to your shell’s startup script.   

You can add the following function to your shell configuration file:   
(`~/.zshrc` for ZSH, `~/.bashrc` for Bash, or `~/.bash_profile` for Bash on macOS):

```shell
# For ZSH and BASH
ash-source() {
    python3 /path/to/ash.py --source
    source ash-source.sh
    rm ash-source.sh
}

# For Windows PowerShell
ash-source() {
    python3 /path/to/ash.py --source
    . ash-source.sh
    rm ash-source.sh
}
```

And then reload the shell configurations using the appropriate file path:
```shell
source ~/.zshrc
```

## Using ash-repl
The `ash-repl` command will run a small REPL where you can run all ASH commands without needing the `ash` prefix.  
For it to run properly, ensure you have set the correct config value for `python-cli-command`.
To exit the repl, type `ash-exit` or `!!`.

## Development
### MVP 1:
- [X] Add parameter substitution
- [X] Add plugin infrastructure

### MVP 2:
- [X] Add basic configs
- [>] Autocomplete / Suggestions
- [X] Find a way to ensure all paramters have been filled in
- [X] Add the `ash-source` feature 
    - Sources/dot-sources every function into the current shell to act as native functions
- [X] Update README (Adding ash as an alias, reserved keywords, using ash-source, file location, installation guide)

### MVP 3:
- [X] Add the `ash ash-repl` feature
    - A custom loop where custom functions can be called without needing the `ash` command prefix 
- [X] Add the `ash ash-info <command>` feature
    - Displays the metadata of a given function, described as `$desc: "..."` in the YAML file

### MVP 4:
- [ ] Get valuble user feedback to plan future progress