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

# AUTOCOMPLETE PARSER
def fetchCommandKeys(commandObject, commandPrefix = ""):
    for commandKey, commandValue in commandObject.items():
        commandFullKey = f"{commandPrefix}:{commandKey}" if commandPrefix else commandKey
        yield commandFullKey
        if "subcmd" in commandValue:
            yield from fetchCommandKeys(commandValue["subcmd"], commandFullKey)

autocompleteLegend = list(fetchCommandKeys(commandLegend, ""))

# ARGUMENT PARSER
if len(sys.argv) < 2: 
    print("Usage: ash <command> <arguments>")
    exit()

ashCommand = sys.argv[1]
ashArgs = sys.argv[2:]

# COMMAND PARSER
if ashCommand.split(ashConfig["compound-separator"])[0] in commandLegend.keys():
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
else:
    print(f"Error - Command \"{ashCommand}\" not found in ASH")