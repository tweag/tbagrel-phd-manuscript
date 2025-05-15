#!/usr/bin/env python3

import re
import os

DIR = "./schemas"

def list_files_with_extension(directory, extension):
    return [
        os.path.join(directory, f) for f in os.listdir(directory)
        if f.endswith(extension) and os.path.isfile(os.path.join(directory, f))
    ]

# Example usage
files = list_files_with_extension(DIR, ".tikz")
for file_path in files:
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
        content = re.sub(r"\\draw(.*?)\(([0-9]+)\) to \(([0-9]+)\)", r"\\draw\g<1>(\g<2>.center) to (\g<3>.center)", content)
        content = re.sub(r"\\draw(.*?)\((.*?)\) to \(([0-9]+)\)", r"\\draw\g<1>(\g<2>) to (\g<3>.center)", content)
        content = re.sub(r"\\draw(.*?)\(([0-9]+)\) to \((.*?)\)", r"\\draw\g<1>(\g<2>) to (\g<3>)", content)
        content = content.replace("?", "⩴")
        content = content.replace("�", "¤")
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)
