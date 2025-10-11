# IMPORTS
import os
import yaml
import subprocess
import json

# INIT
commandLegend = {}
with open("./ash.config.yaml", "r") as ashConfigFile:
    rawCommandLegend = yaml.safe_load(ashConfigFile)
    ashConfig = rawCommandLegend["ash-config"]
    del rawCommandLegend["ash-config"]
    commandLegend = rawCommandLegend

# LOGIC
while True:
    try:
        userEnteredCommand = input(ashConfig["prompt"])
        terminalCommand, *terminalArgs = userEnteredCommand.split(" ")

        if terminalCommand == "ash-exit" or terminalCommand == "!!": break
        
        if terminalCommand.split(":")[0] in commandLegend.keys():
            try:
                if ":" in terminalCommand:
                    terminalCommandRoot, *terminalCommandBranch = terminalCommand.split(":")
                    # Compound Command

                    keys = terminalCommand.split(":")
                    node = commandLegend
                    
                    for idx, key in enumerate(keys):
                        node = node.get(key)
                        if node is None:
                            break
                        if idx < len(keys) - 1:
                            node = node.get('subcmd', {})
                    cmd = node.get('cmd') if isinstance(node, dict) else None

                    print(f"Custom: {terminalCommand}; CMD: {cmd}")
                else:
                    # Basic Command
                    print(f"Custom: {terminalCommand}; CMD: {commandLegend[terminalCommand]['cmd']}")
            except:
                print(f"Error - \"{terminalCommand}\" is not recognized as a custom command (No `cmd:` in YAML)")
        else:
            print(f"Native: {terminalCommand}; CMD: [Native]")

    except KeyboardInterrupt:
        print("\n[Cancelled]")
        break