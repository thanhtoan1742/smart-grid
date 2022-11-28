import yaml
import os

from typing import Dict, Any

cfg = None


def deep_update_dict(a: Any, b: Any) -> Any:
    if not isinstance(a, dict):
        return b or a

    res = {}
    for ck in a:
        va = a[ck]
        if not b or ck not in b:
            vb = None
        else:
            vb = b[ck]
        res[ck] = deep_update_dict(va, vb)
    return res


def config() -> Dict:
    global cfg
    if cfg != None:
        return cfg

    with open("config_default.yaml") as f:
        cfg = yaml.safe_load(f)

    user = {}
    if os.path.exists("config.yaml"):
        with open("config.yaml") as f:
            user = yaml.safe_load(f)
    cfg = deep_update_dict(cfg, user)
    return cfg
