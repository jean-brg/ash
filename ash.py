# IMPORTS
import os
import yaml
import subprocess
import sys
import re

# INITIALIZER
commandLegend = {}
ashConfig = {}
with open("./ash.config.yaml", "r") as ashConfigFile:
    rawCommandLegend = yaml.safe_load(ashConfigFile)
    ashConfig = rawCommandLegend["ash-config"]
    del rawCommandLegend["ash-config"]
    commandLegend = rawCommandLegend

# FLAT COMMAND LEGEND PARSER
def flattenCommandLegend(commandObject, commandPrefix = ""):
    for item in commandObject.items():
        if "cmd" in item[1].keys():
            yield (f"{commandPrefix}:{item[0]}" if commandPrefix else item[0], item[1]["cmd"])
        subCommands = [subcmd for subcmd in item[1].keys() if subcmd != "cmd" and not subcmd.startswith("$")]
        if len(subCommands) >= 1:
            for subcmd in subCommands:
                yield from flattenCommandLegend({subcmd: commandObject[item[0]][subcmd]}, f"{commandPrefix}:{item[0]}" if commandPrefix else item[0])

# ASH-SOURCE DECLARATION
def ashSource():
    with open("ash-source.sh", "w") as sourceFile:
        sourceFile.write("\n\n".join(["{}() {{\n{}\n}}".format(command[0], '\n'.join('    ' + line if line.strip() != "" else line for line in command[1].splitlines())) for command in list(flattenCommandLegend(commandLegend, ""))]))

# ARGUMENT PARSER
if len(sys.argv) < 2:
    print("ASH - Ready to automate")
    print("Usage: ash <command> <arguments>")
    os._exit(1)
elif sys.argv[1] == "--source":
    ashSource()
    os._exit(1)

ashCommand = sys.argv[1]
ashArgs = sys.argv[2:]

# COMMAND PARSER
if ashCommand.split(ashConfig["compound-separator"])[0] in commandLegend.keys():
    # CUSTOM COMMANDS
    try:
        if ashConfig["compound-separator"] in ashCommand:
            # COMPOUND COMMAND HANDLER
            commandKeys = ashCommand.split(ashConfig["compound-separator"])
            commandNode = commandLegend
            
            for idx, key in enumerate(commandKeys):
                commandNode = commandNode.get(key)
                if commandNode is None:
                    break
                if idx < len(commandKeys) - 1:
                    commandNode = commandNode.get('subcmd', {})
            shellCommand = commandNode.get('cmd') if isinstance(commandNode, dict) else None

        else:
            # BASIC COMMAND HANDLER
            shellCommand = commandLegend[ashCommand]["cmd"]

        # ARGUMENT MATCHER
        argMatches = [int(match) for match in re.findall("\$([0-9]+)", shellCommand)]
        if len(ashArgs) < max(argMatches):
            print(f"Error - Command \"{ashCommand}\" requires {len(argMatches)} arguments, but was given {len(ashArgs)}")
            os._exit(1)

        for argIndex in argMatches:
            shellCommand = shellCommand.replace(f"${argIndex}", ashArgs[argIndex - 1])

        # EXECUTION CONFIRMATION
        if ashConfig["confirm-execution"]:
            runExecusion = input(f"Run \"{shellCommand}\"? (Enter/n) ")
            if runExecusion != "": 
                print("[Execution Terminated]")
                os._exit(1)

        # EXECUTION
        subprocess.run(shellCommand, shell=True, executable=ashConfig["shell-executable"])

    except:
        print(f"Error - Command \"{ashCommand}\" failed to execute")
elif ashCommand.startswith("ash-"):
    # BUILT-IN COMMANDS
    match ashCommand:
        # SEE BELOW FOR ASH-SOURCE
        case "ash-repl":
            print("Do repl stuff")
        
        case _:
            print(f"Error - Unknown built-in command \"{ashCommand}\"")

else:
    print(f"Error - Command \"{ashCommand}\" not found in ASH")