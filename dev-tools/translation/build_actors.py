#!/usr/bin/env python3
"""Align legacy Spanish actor translations with current Foundry 14 IDs."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any
from reviewed_cleanup import apply_reviewed_cleanup


PROTECTED = re.compile(r"@(?:UUID|Embed)\[([^\]]+)\]|&Reference\[([^\]]+)\]|\[\[([^\]]+)\]\]")


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def tokens(value: str) -> Counter[str]:
    return Counter(next(part for part in match if part is not None) for match in PROTECTED.findall(value))


def candidates(source: dict[str, Any], legacy_key: str) -> list[str]:
    if legacy_key in source:
        return [legacy_key]
    matches = [key for key, row in source.items() if legacy_key in (row.get("name"), row.get("type"))]
    if matches:
        return matches
    return [next(iter(source))] if len(source) == 1 else []


def main() -> int:
    parser = argparse.ArgumentParser()
    module_root = Path(__file__).resolve().parents[2]
    dev_tools = module_root / "dev-tools"
    parser.add_argument("--en", type=Path, default=dev_tools / "export/data/dnd-tashas-cauldron.tcoe-actors.en.json")
    parser.add_argument("--es", type=Path, default=dev_tools / "export/_data/dnd-tashas-cauldron.tcoe-actors.json")
    parser.add_argument("--output", type=Path, default=module_root / "compendium/dnd-tashas-cauldron.tcoe-actors.json")
    parser.add_argument("--assets", type=Path, default=dev_tools / "translation/generated")
    args = parser.parse_args()

    source, legacy = load(args.en), load(args.es)
    conflicts: list[dict[str, Any]] = []
    token_issues: list[dict[str, Any]] = []
    memory: list[dict[str, Any]] = []
    glossary: dict[str, dict[str, Any]] = {}

    output: dict[str, Any] = {
        "label": "Actores de Tasha",
        "mapping": {
            "biography": "system.details.biography.value",
            "tokenName": "prototypeToken.name",
            "items": {"path": "items", "converter": "tcoeActorItemsById"},
            "effects": {"path": "effects", "converter": "tcoeEffectsById"},
        },
        "folders": {},
        "entries": {},
    }

    for folder, source_value in source.get("folders", {}).items():
        target = legacy.get("folders", {}).get(folder, source_value)
        output["folders"][folder] = target
        if source_value != target:
            glossary[source_value] = {"es": target, "category": "folder", "confidence": 1.0}

    def add_pair(source_text: str, target_text: str, entry_id: str, path: str, category: str = "") -> None:
        if source_text == target_text:
            return
        memory.append({
            "source": source_text, "target": target_text, "pack": "tcoe-actors",
            "documentId": entry_id, "path": path, "confidence": 1.0,
        })
        if category and source_text and len(source_text) <= 100:
            glossary.setdefault(source_text, {"es": target_text, "category": category, "confidence": 1.0})
        if tokens(source_text) != tokens(target_text):
            token_issues.append({"entryId": entry_id, "path": path})

    for entry_id, source_entry in source.get("entries", {}).items():
        legacy_entry = legacy.get("entries", {}).get(entry_id)
        if not isinstance(legacy_entry, dict):
            conflicts.append({"entryId": entry_id, "reason": "missing-spanish-entry"})
            continue
        target: dict[str, Any] = {}
        if isinstance(legacy_entry.get("name"), str):
            target["name"] = legacy_entry["name"]
            add_pair(source_entry.get("name", ""), target["name"], entry_id, "name", "actor-name")
        if isinstance(legacy_entry.get("tokenName"), str):
            target["tokenName"] = legacy_entry["tokenName"]
        if isinstance(legacy_entry.get("description"), str):
            target["biography"] = legacy_entry["description"]
            add_pair(source_entry.get("biography", ""), target["biography"], entry_id, "biography")

        source_items = source_entry.get("items", {}) or {}
        target_items: dict[str, Any] = {}
        for legacy_key, legacy_item in (legacy_entry.get("items", {}) or {}).items():
            matches = candidates(source_items, legacy_key)
            if not matches:
                conflicts.append({"entryId": entry_id, "field": "items", "legacyKey": legacy_key})
                continue
            for item_id in matches:
                source_item = source_items[item_id]
                item_patch: dict[str, Any] = {}
                for field in ("name", "description"):
                    if isinstance(legacy_item.get(field), str):
                        item_patch[field] = legacy_item[field]
                        add_pair(source_item.get(field, ""), legacy_item[field], entry_id, f"items.{item_id}.{field}", f"item-{field}" if field == "name" else "")
                for nested_field in ("activities", "effects", "advancement"):
                    source_nested = source_item.get(nested_field, {}) or {}
                    translated_nested: dict[str, Any] = {}
                    for nested_key, nested_patch in (legacy_item.get(nested_field, {}) or {}).items():
                        nested_matches = candidates(source_nested, nested_key)
                        if not nested_matches:
                            conflicts.append({
                                "entryId": entry_id, "itemId": item_id,
                                "field": nested_field, "legacyKey": nested_key,
                            })
                            continue
                        for nested_id in nested_matches:
                            translated_nested[nested_id] = nested_patch
                            source_row = source_nested[nested_id]
                            for key in ("name", "description", "condition", "chatFlavor", "title", "hint"):
                                if isinstance(source_row.get(key), str) and isinstance(nested_patch.get(key), str):
                                    add_pair(source_row[key], nested_patch[key], entry_id, f"items.{item_id}.{nested_field}.{nested_id}.{key}", f"{nested_field}-{key}" if key in ("name", "title") else "")
                    if translated_nested:
                        item_patch[nested_field] = translated_nested
                target_items[item_id] = item_patch
        if target_items:
            target["items"] = target_items

        source_effects = source_entry.get("effects", {}) or {}
        target_effects: dict[str, Any] = {}
        for legacy_key, patch in (legacy_entry.get("effects", {}) or {}).items():
            matches = candidates(source_effects, legacy_key)
            if not matches:
                conflicts.append({"entryId": entry_id, "field": "effects", "legacyKey": legacy_key})
                continue
            for effect_id in matches:
                target_effects[effect_id] = patch
        if target_effects:
            target["effects"] = target_effects
        output["entries"][entry_id] = target

    report = {
        "pack": "dnd-tashas-cauldron.tcoe-actors",
        "sourceEntries": len(source.get("entries", {})),
        "legacyEntries": len(legacy.get("entries", {})),
        "outputEntries": len(output["entries"]),
        "translatedItems": sum(len(entry.get("items", {})) for entry in output["entries"].values()),
        "translationMemoryPairs": len(memory),
        "glossaryTerms": len(glossary),
        "conflicts": len(conflicts),
        "protectedTokenIssues": len(token_issues),
    }
    apply_reviewed_cleanup("actors", output, memory)
    write(args.output, output)
    write(args.assets / "translation-memory.actors.json", memory)
    write(args.assets / "glossary.actors.json", dict(sorted(glossary.items())))
    write(args.assets / "conflicts.actors.json", conflicts)
    write(args.assets / "protected-token-issues.actors.json", token_issues)
    write(args.assets / "report.actors.json", report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 2 if conflicts or token_issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
