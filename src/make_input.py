import re

INPUT_FILE = ""

with open(INPUT_FILE) as f:
    fc = f.read()

match = re.search(r"\{*\}", fc)
s = match.group()
print(len(s), s[:10], s[:-10])