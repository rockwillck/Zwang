#!/usr/bin/env python3

from os import listdir
from os.path import isfile, join

src = input("Folder Path: ")
name = input("Package Name: ")
files = [open(join(src, f), "r").read() for f in listdir(src) if isfile(join(src, f)) and f.endswith(".js")]

documentation = f"""# {name}
"""

def sliceUntil(str, until):
    return str[:str.index(until)].strip()

def document(f):
    global documentation
    lastClass = ""
    lastClassAdded = False
    lines = [l.strip() for l in f.split("\n")]
    soFarDocumented = ""
    for i, line in enumerate(lines):
        # print(line)
        if line.startswith("class"):
            lastClass = sliceUntil(line.replace('class', '', 1), "{").strip()
        elif line.startswith("/* ++"):
            if not lastClassAdded:
                documentation += f"""## {lastClass}
"""
                lastClassAdded = True
            soFarDocumented += line.replace("/* ++", "", 1).strip() + "  \n"
        elif line.strip().endswith("-- */"):
            soFarDocumented += line.strip().replace("-- */", "") + "  \n"
            methodName = sliceUntil(lines[i + 1], "{")
            documentation += f"""### {methodName}
{soFarDocumented}"""
            soFarDocumented = ""
        elif not soFarDocumented == "":
            soFarDocumented += line.strip() + "  \n"
            # print(soFarDocumented)

for file in files:
    document(file)

open(src + "/" + src + "-documentation.md", "w").write(documentation)