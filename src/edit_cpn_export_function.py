import os
import xml.etree.ElementTree as ET

DIR = "data/nets/"

SCRIPT = """\
val outputpath = "C:/Users/at/Dev/smart-grid/data/dots/";
val filename = "{name}";
OGtoGraphviz.ExportStateSpace(outputpath ^ filename ^ ".dot");
"""


def edit_script(name: str) -> None:
    file = DIR + name + ".cpn"

    tree = ET.parse(file)
    root = tree.getroot()
    script_elem = root.find(".//*[@name='ExportToGraphviz']/../Aux/text")
    if script_elem != None:
        script = SCRIPT.format(name=name)
        script_elem.text = script
        tree.write(file)
        print(file, "modified")
    else:
        print(file, "unmodified")


names = [
    file[:-4]
    for file in os.listdir(DIR)
    if file.endswith(".cpn") and not file.count("original")
]

for name in names:
    edit_script(name)
