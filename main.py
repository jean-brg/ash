# IMPORTS
import os
import yaml
import subprocess
import sys

# INIT
commandLegend = {}
ashConfig = {}
with open("./ash.config.yaml", "r") as ashConfigFile:
    rawCommandLegend = yaml.safe_load(ashConfigFile)
    ashConfig = rawCommandLegend["ash-config"]
    del rawCommandLegend["ash-config"]
    commandLegend = rawCommandLegend

# LOGIC
if len(sys.argv) < 2: 
    print("Usage: ash <command> <arguments>")
    exit()

ashCommand = sys.argv[1]
ashArgs = sys.argv[2:]

if ashCommand.split(ashConfig["compound-separator"])[0] in commandLegend.keys():
    try:
        if ashConfig["compound-separator"] in ashCommand:
            # Compound Command
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
            # Basic Command
            shellCommand = commandLegend[ashCommand]["cmd"]

        for argIndex, arg in enumerate(ashArgs):
            shellCommand = shellCommand.replace(f"${argIndex + 1}", arg)

        if ashConfig["confirm-execution"]:
            runExecusion = input(f"Run \"{shellCommand}\"? (Enter/n) ")
            if runExecusion != "": 
                print("[Execution Terminated]")
                os._exit(1)
        subprocess.run(shellCommand, shell=True, executable=ashConfig["shell-executable"])

    except:
        print(f"Error - Command \"{ashCommand}\" not recognized as a custom command (No `cmd:` in YAML)")
else:
    print(f"Error : Command \"{ashCommand}\" not found in ASH")