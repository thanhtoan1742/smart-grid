import pygraphviz as pg
from pathlib import Path
import subprocess
import shutil
import os


def ls2l(s):
    return [e.strip()[1:-1] for e in s[1:-1].split(",")]


def read_path(filename):
    with open(filename) as f:
        lines = f.readlines()

    path = []
    searched_nodes = []
    dest = ""
    for lines in lines:
        key, value = [e.strip() for e in lines.split(":")]
        if key == "Path":
            path = ls2l(value)
        if key == "Searched nodes":
            searched_nodes = ls2l(value)
        if key == "Final node":
            dest = value

    return path, searched_nodes, dest


def generate_report_dot(in_dot_file, in_path_file, out_dot_file):
    G = pg.AGraph(filename=in_dot_file)
    path, searched_nodes, dest = read_path(in_path_file)

    for node in G.nodes():
        if node != dest:
            node.attr["label"] = str(node)
        if node in searched_nodes:
            idx = searched_nodes.index(node)
            node.attr["style"] = "filled"
            node.attr["fillcolor"] = "cyan"
            if node == dest:
                node.attr["label"] = "N" + node.attr["label"]
            node.attr["label"] = f"[{idx + 1}] {node.attr['label']}"

        if node in path:
            node.attr["fontcolor"] = "black"
            node.attr["fillcolor"] = "chartreuse"
            node.attr["style"] = "filled"

    for edge in G.edges():
        edge.attr["label"] = ""
    for i in range(len(path) - 1):
        e = G.get_edge(path[i], path[i + 1])
        e.attr["fillcolor"] = "chartreuse"
        e.attr["style"] = "filled"

    G.write(out_dot_file)


OUT_PATH_PREFIX = "data/result"
for name in ["case3_1"]:
    out_name_dir = f"{OUT_PATH_PREFIX}/{name}"
    os.makedirs(out_name_dir, exist_ok=True)
    in_dot_file = f"data/dots/{name}.dot"
    shutil.copy(f"data/reports/{name}.txt", f"{out_name_dir}/report.txt")
    shutil.copy(in_dot_file, f"{out_name_dir}/net.dot")
    for postfix in ["h1", "h2", "h1_rever", "h2_rever"]:
        out_path = f"{out_name_dir}/{postfix}"
        os.makedirs(out_path, exist_ok=True)

        in_path_file = f"{out_path}/path.txt"
        shutil.copy(f"data/path/{name}_{postfix}.txt", in_path_file)

        out_dot_file = f"{out_path}/result.dot"
        print(out_dot_file)
        generate_report_dot(in_dot_file, in_path_file, out_dot_file)

        out_png_file = f"{out_path}/result.png"
        res = subprocess.run(["dot", out_dot_file, "-Tpng", "-o", out_png_file])
