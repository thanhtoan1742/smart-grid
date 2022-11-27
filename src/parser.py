from functools import reduce
from typing import Any, Literal

from lark import Lark, Transformer


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
    parser="lalr",
    transformer=Marshaller(),
    start=["node_label", "edge_label"],
)


def parse(text: str, start: Literal["node_label", "edge_label"]) -> Any:
    if text == "":
        return {}
    return parser.parse(text, start=start)


# print(parse("A6:2->7:trans: {p3=2,con={i=5,t=CON,c=1},p4=0}", start="edge_label"))
# print(parse("A8:2->9:CB4b: {p=1}", start="edge_label"))
# print(
#     parse(
#         """72:
# Generator: empty
# Generated: 1`0
# Consumer: 1`({i=3,t=BAT,c=100},3)++
# 1`({i=4,t=CON,c=3},2)++
# 1`({i=5,t=CON,c=1},1)++
# 1`({i=6,t=CON,c=2},2)
# """,
#         start="node_label",
#     )
# )

# print(parse("A17:5->15:gen: {p2=1,gen={i=1,t=GEN,c=5},p1=5}", start="edge_label"))
