"""Apply reviewed ID-based translations after legacy alignment."""

import json
from pathlib import Path


def apply_reviewed_cleanup(pack, output, memory=None):
    patches = json.loads(Path(__file__).with_name("reviewed-english-cleanup.json").read_text(encoding="utf-8"))
    replacements = {}

    def merge(target, patch):
        for key, value in patch.items():
            if isinstance(value, dict):
                merge(target.setdefault(key, {}), value)
            else:
                previous = target.get(key)
                if isinstance(previous, str):
                    replacements[previous] = value
                target[key] = value

    merge(output, patches.get(pack, {}))
    for row in memory or []:
        if row.get("target") in replacements:
            row["target"] = replacements[row["target"]]
