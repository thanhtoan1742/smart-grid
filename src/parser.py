from lark import Lark, Transformer
from functools import reduce
from typing import Any, Literal


class Marshaller(Transformer):
    node_label = lambda self, n_kvps: reduce(
        lambda acc, d: {**acc, **d}, n_kvps[1:], {}
    )

    edge_label = lambda self, n3_k_r: {n3_k_r[3]: n3_k_r[4]}

    kvp = lambda self, kv: {kv[0]: kv[1]}

    marking = lambda self, l: l[0] if len(l) == 1 else list(zip(l[0::2], l[1::2]))
    empty = lambda self, _: None

    product = tuple
    record = lambda self, lkv: dict(zip(lkv[0::2], lkv[1::2]))

    string = lambda self, s: str(s[0])
    number = lambda self, n: int(n[0])


parser = Lark.open(
    "grammar.lark",
    rel_to=__file__,
    start=["node_label", "edge_label"],
)
marshaller = Marshaller()


def parse(text: str, start: Literal["node_label", "edge_label"]) -> Any:
    if text == "":
        return {}
    return marshaller.transform(parser.parse(text, start=start))
