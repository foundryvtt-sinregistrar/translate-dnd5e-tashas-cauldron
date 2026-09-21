#!/usr/bin/env python3
"""Align legacy Spanish TCoE translations with the current Foundry 14 export."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any
from reviewed_cleanup import apply_reviewed_cleanup


PROTECTED = re.compile(
    r"@(?:UUID|Embed)\[([^\]]+)\]|&Reference\[([^\]]+)\]|\[\[([^\]]+)\]\]"
)


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def protected_tokens(value: str) -> Counter[str]:
    return Counter(next(part for part in match if part is not None) for match in PROTECTED.findall(value))


def translated_fields(value: Any, allowed: tuple[str, ...], nested: tuple[str, ...] = ()) -> dict[str, Any]:
    if not isinstance(value, dict):
        return {}
    result: dict[str, Any] = {
        key: value[key] for key in allowed if isinstance(value.get(key), str)
    }
    for key in nested:
        if isinstance(value.get(key), (dict, list, str)):
            result[key] = value[key]
    return result


def align_nested(
    entry_id: str,
    field: str,
    source: dict[str, Any],
    legacy: dict[str, Any],
    conflicts: list[dict[str, Any]],
) -> dict[str, Any]:
    source_rows = source.get(field) if isinstance(source.get(field), dict) else {}
    legacy_rows = legacy.get(field) if isinstance(legacy.get(field), dict) else {}
    allowed = ("name", "description", "condition", "chatFlavor") if field != "advancement" else ("title", "hint")
    result: dict[str, Any] = {}

    for legacy_key, legacy_value in legacy_rows.items():
        matches: list[str] = []
        method = ""
        if legacy_key in source_rows:
            matches, method = [legacy_key], "id"
        else:
            matches = [
                source_id for source_id, source_value in source_rows.items()
                if legacy_key in (source_value.get("name"), source_value.get("title"))
            ]
            method = "source-label"
        if not matches and field == "activities":
            matches = [
                source_id for source_id, source_value in source_rows.items()
                if legacy_key == source_value.get("type")
            ]
            method = "activity-type"
            if len(matches) > 1:
                unnamed = [source_id for source_id in matches if not source_rows[source_id].get("name")]
                if len(unnamed) == 1:
                    matches, method = unnamed, "activity-type-unnamed"
        if not matches and len(source_rows) == len(legacy_rows) == 1:
            matches, method = [next(iter(source_rows))], "single-row"

        patch = translated_fields(
            legacy_value,
            allowed,
            nested=("roll", "profiles") if field == "activities" else (),
        )
        if matches and patch:
            for source_id in matches:
                result[source_id] = patch
        else:
            conflicts.append({
                "entryId": entry_id,
                "field": field,
                "legacyKey": legacy_key,
                "reason": "missing-source-row" if not source_rows else "ambiguous-or-unmatched",
                "sourceCandidates": [
                    {"id": source_id, "type": row.get("type", ""), "name": row.get("name", ""), "title": row.get("title", "")}
                    for source_id, row in source_rows.items()
                ],
                "translation": legacy_value,
            })
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    module_root = Path(__file__).resolve().parents[2]
    dev_tools = module_root / "dev-tools"
    parser.add_argument("--en", type=Path, default=dev_tools / "export/data/dnd-tashas-cauldron.tcoe-character-options.en.json")
    parser.add_argument("--es", type=Path, default=dev_tools / "export/_data/dnd-tashas-cauldron.tcoe-character-options.json")
    parser.add_argument("--output", type=Path, default=module_root / "compendium/dnd-tashas-cauldron.tcoe-character-options.json")
    parser.add_argument("--assets", type=Path, default=dev_tools / "translation/generated")
    args = parser.parse_args()

    source = load(args.en)
    legacy = load(args.es)
    conflicts: list[dict[str, Any]] = []
    token_issues: list[dict[str, Any]] = []
    memory: list[dict[str, Any]] = []
    glossary: dict[str, dict[str, Any]] = {}

    output: dict[str, Any] = {
        "label": "Opciones de personaje",
        "mapping": {
            "description": "system.description.value",
            "activities": {"path": "system.activities", "converter": "tcoeActivitiesById"},
            "effects": {"path": "effects", "converter": "tcoeEffectsById"},
            "advancement": {"path": "system.advancement", "converter": "tcoeAdvancementById"},
        },
        "folders": {},
        "entries": {},
    }

    for source_folder, source_folder_value in source.get("folders", {}).items():
        target = legacy.get("folders", {}).get(source_folder, source_folder_value)
        output["folders"][source_folder] = target
        if target != source_folder_value:
            glossary[source_folder_value] = {"es": target, "category": "folder", "confidence": 1.0}

    for entry_id, source_entry in source.get("entries", {}).items():
        legacy_entry = legacy.get("entries", {}).get(entry_id)
        if not isinstance(legacy_entry, dict):
            conflicts.append({"entryId": entry_id, "reason": "missing-spanish-entry"})
            continue

        target_entry: dict[str, Any] = {}
        for field in ("name", "description"):
            source_text = source_entry.get(field)
            target_text = legacy_entry.get(field)
            if not isinstance(source_text, str) or not isinstance(target_text, str):
                continue
            target_entry[field] = target_text
            if source_text != target_text:
                memory.append({
                    "source": source_text,
                    "target": target_text,
                    "pack": "tcoe-character-options",
                    "documentId": entry_id,
                    "path": field,
                    "confidence": 1.0,
                })
                if field == "name" and len(source_text) <= 100:
                    glossary[source_text] = {"es": target_text, "category": "document-name", "confidence": 1.0}
            if protected_tokens(source_text) != protected_tokens(target_text):
                token_issues.append({
                    "entryId": entry_id,
                    "path": field,
                    "sourceTokens": protected_tokens(source_text),
                    "targetTokens": protected_tokens(target_text),
                })

        for field in ("activities", "effects", "advancement"):
            aligned = align_nested(entry_id, field, source_entry, legacy_entry, conflicts)
            if aligned:
                target_entry[field] = aligned
                for nested_id, translated in aligned.items():
                    source_nested = source_entry.get(field, {}).get(nested_id, {})
                    for key, target_text in translated.items():
                        source_text = source_nested.get(key)
                        if isinstance(source_text, str) and source_text != target_text:
                            memory.append({
                                "source": source_text,
                                "target": target_text,
                                "pack": "tcoe-character-options",
                                "documentId": entry_id,
                                "path": f"{field}.{nested_id}.{key}",
                                "confidence": 1.0,
                            })
                            if key in ("name", "title") and source_text:
                                glossary.setdefault(source_text, {
                                    "es": target_text,
                                    "category": f"{field}-{key}",
                                    "confidence": 1.0,
                                })

        output["entries"][entry_id] = target_entry

    report = {
        "pack": "dnd-tashas-cauldron.tcoe-character-options",
        "sourceEntries": len(source.get("entries", {})),
        "legacyEntries": len(legacy.get("entries", {})),
        "outputEntries": len(output["entries"]),
        "translationMemoryPairs": len(memory),
        "glossaryTerms": len(glossary),
        "conflicts": len(conflicts),
        "protectedTokenIssues": len(token_issues),
        "requiresFreshExport": any(
            conflict.get("field") == "advancement" and conflict.get("reason") == "missing-source-row"
            for conflict in conflicts
        ),
    }

    apply_reviewed_cleanup("character-options", output, memory)
    write(args.output, output)
    write(args.assets / "translation-memory.character-options.json", memory)
    write(args.assets / "glossary.character-options.json", dict(sorted(glossary.items())))
    write(args.assets / "conflicts.character-options.json", conflicts)
    write(args.assets / "protected-token-issues.character-options.json", token_issues)
    write(args.assets / "report.character-options.json", report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 2 if report["requiresFreshExport"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
