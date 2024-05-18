#!/usr/bin/env python3

from os import listdir
from os.path import isfile, join
import sys

if len(sys.argv) > 1:
    src = sys.argv[1]
else:
    src = input("Folder Path: ")
if len(sys.argv) > 2:
    name = sys.argv[2]
else:
    name = input("Name: ")

files = [open(join(src, f), "r").read() for f in listdir(src) if isfile(join(src, f)) and f.endswith(".js")]

documentation = f"""# {name}
"""

def sliceUntil(str, until):
    return str[:str.index(until)].strip()

def document(f):
    global documentation
    lastClass = ""
    lastClassAdded = False
    inSpecial = False
    lines = [l for l in f.split("\n")]
    soFarDocumented = ""
    for i, line in enumerate(lines):
        stripped = line.strip()
        # print(line)
        if stripped.startswith("class"):
            lastClass = sliceUntil(line.replace('class', '', 1), "{").strip()
            lastClassAdded = False
        elif stripped.startswith("/* ++"):
            if not lastClassAdded:
                documentation += f"""## {lastClass}
"""
                lastClassAdded = True
            soFarDocumented += "__"+line.replace("/* ++", "", 1).strip() + "__  \n"
        elif stripped.startswith("/* +"):
            soFarDocumented = f"## {line[4:]}\n"
            inSpecial = True
        elif stripped.endswith("-- */"):
            if not inSpecial:
                soFarDocumented += line.strip().replace("-- */", "") + "  \n"
                methodName = sliceUntil(lines[i + 1], "{")
                documentation += f"""### {methodName}
{soFarDocumented}"""
            else:
                documentation += "\n" + soFarDocumented
                inSpecial = False
            soFarDocumented = ""
        elif inSpecial:
            soFarDocumented += line + "  \n"
        elif not soFarDocumented == "":
            soFarDocumented += line.strip() + "  \n"
            # print(soFarDocumented)

for file in files:
    document(file)

open(src + "/" + src + "-documentation.md", "w").write(documentation)