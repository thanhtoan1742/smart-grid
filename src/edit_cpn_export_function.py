import os
import xml.etree.ElementTree as ET
import yaml

with open("config.yaml") as f:
    cfg = yaml.safe_load(f)

DIR = "data/nets/"
OUTPUT_PATH = cfg["dir"]["base"] + "/data/dots/"
print(OUTPUT_PATH)

SCRIPT = """\
val output_path = "{output_path}";
val file_name = "{name}";
fun iota(n: int) = if n < 1 then [] else (iota (n-1)) ++ [n];
OGSet.StringRepOptions'PI(fn (page, place, inst) => place);
OGSet.StringRepOptions'TI(
    fn (page,trans,inst) => trans
);
OGtoGraphviz.ExportNodes(output_path ^ file_name ^ "_nodes.dot", iota(NoOfNodes()));
OGtoGraphviz.ExportArcs(output_path ^ file_name ^ "_arcs.dot", iota(NoOfArcs()));
OGtoGraphviz.ExportStateSpace(output_path ^ file_name ^ ".dot");
"""


def edit_script(name: str) -> bool:
    file_name = DIR + name + ".cpn"

    tree = ET.parse(file_name)
    root = tree.getroot()
    page = root.find(".//*[@name='ExportToGraphviz']/..")
    if not page:
        return False
    auxs = page.findall("./Aux")
    if len(auxs) == 0:
        return False

    aux_id = auxs[0].get("id")

    for aux in auxs:
        page.remove(aux)

    aux = ET.Element("Aux", id=aux_id)
    text = ET.Element("text")
    text.text = SCRIPT.format(name=name, output_path=OUTPUT_PATH)
    aux.extend(
        [
            ET.Element("posattr", x="0.00000", y="0.00000"),
            ET.Element("fillattr", colour="White", pattern="", filled="false"),
            ET.Element("lineattr", colour="Black", thick="1", type="Solid"),
            ET.Element("textattr", colour="Black", bold="false"),
            ET.Element("label"),
            text,
        ]
    )
    page.append(aux)
    tree.write(file_name)

    return True


names = [file_name[:-4] for file_name in os.listdir(DIR) if file_name.endswith(".cpn")]

for name in names:
    modded = False
    if not name.count("original") and not name.count("sample"):
        modded = edit_script(name)
    if modded:
        print("Modified:  ", name)
    else:
        print("Unmodified:", name)
