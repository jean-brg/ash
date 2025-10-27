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

# ASH METADATA PARSER
def fetchCommandMetadata(commandObject, targetCommand, commandPath=None):
    if commandPath is None: targetParts = targetCommand.split(":")
    else: targetParts = targetCommand
    for key, value in commandObject.items():
        if key.startswith("$"):
            continue
        if key == targetParts[0]:
            if len(targetParts) == 1:
                return {k[1:]: v for k, v in value.items() if k.startswith("$")}
            result = fetchCommandMetadata(value, targetParts[1:], targetParts)
            if result:
                return result
    return None

# ASH-SOURCE DECLARATION
def ashSource():
    with open("ash-source.sh", "w") as sourceFile:
        sourceFile.write("\n\n".join(["{}() {{\n{}\n}}".format(command[0], '\n'.join('    ' + line if line.strip() != "" else line for line in command[1].splitlines())) for command in list(flattenCommandLegend(commandLegend, ""))]))

# ARGUMENT PARSER
if len(sys.argv) < 2:
    print("ASH - Ready to automate")
    print("Usage: ash <command> <arguments>")
    os._exit(0)
elif sys.argv[1] == "--source":
    ashSource()
    os._exit(0)

ashCommand = sys.argv[1]
ashArgs = sys.argv[2:]

# COMMAND PARSER
if ashCommand.split(ashConfig["compound-separator"])[0] in commandLegend.keys():
    # CUSTOM COMMANDS
    try:
        if ashConfig["compound-separator"] in ashCommand:
            commandKeys = ashCommand.split(ashConfig["compound-separator"])
            commandNode = commandLegend
            for key in commandKeys:
                if key not in commandNode:
                    print(f"DEBUG: '{key}' not found in {list(commandNode.keys())}")
                    commandNode = None
                    break
                commandNode = commandNode[key]
            if isinstance(commandNode, dict):
                shellCommand = commandNode.get("cmd")
            else: 
                shellCommand = None
        else:
            shellCommand = commandLegend[ashCommand]["cmd"]

        # ARGUMENT MATCHER
        argMatches = [int(match) for match in re.findall("\$([0-9]+)", shellCommand)]
        if argMatches:
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
            print("Unadded feature: ASH REPL")
        
        case "ash-info":
            if len(ashArgs) == 0:
                print("Error - Please specify a command to get metadata for.")
                os._exit(1)

            queriedCommand = ashArgs[0]
            queriedMetadata = fetchCommandMetadata(commandLegend, queriedCommand)

            if not queriedMetadata:
                print(f"Error - No metadata found for \"{queriedCommand}\".")
            else:
                print(f"Command: {queriedCommand}")
                for metadataKey, metadataValue in queriedMetadata.items():
                    print(f"  {metadataKey}: {metadataValue}")

        case _:
            print(f"Error - Unknown built-in command \"{ashCommand}\"")

else:
    print(f"Error - Command \"{ashCommand}\" not found in ASH")