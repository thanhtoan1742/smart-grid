from functools import reduce
from typing import Dict, Literal

from lark import Lark, Transformer


class Marshaller(Transformer):
    node_label = lambda _, n_kvps: reduce(lambda acc, d: {**acc, **d}, n_kvps[1:], {})
    edge_label = lambda _, n3_k_r: {n3_k_r[3]: n3_k_r[4]}
    kvp = lambda _, kv: {kv[0]: kv[1]}
    marking = lambda _, l: l[0] if len(l) == 1 else list(zip(l[0::2], l[1::2]))
    empty = lambda _, __: None
    product = tuple
    record = lambda _, lkv: dict(zip(lkv[0::2], lkv[1::2]))
    string = lambda _, s: str(s[0])
    number = lambda _, n: int(n[0])


parser = Lark.open(
    "grammar.lark",
    rel_to=__file__,
    parser="lalr",
    transformer=Marshaller(),
    start=["node_label", "edge_label"],
)


def parse(text: str, start: Literal["node_label", "edge_label"]) -> Dict:
    if text == "":
        return {}
    return parser.parse(text, start=start)
