#!/usr/bin/env python3
"""Build a safe, source-attributed first pass for the magic-items pack."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    module_root = Path(__file__).resolve().parents[2]
    dev_tools = module_root / "dev-tools"
    source = load(dev_tools / "export/data/dnd-tashas-cauldron.tcoe-magic-items.en.json")
    legacy = load(dev_tools / "export/_data/dnd-tashas-cauldron.tcoe-magic-items.json")
    official = load(dev_tools / "translation/official-magic-item-names.json")
    reviewed_descriptions = load(dev_tools / "translation/reviewed-magic-item-descriptions.json")

    # Reuse exact, reviewed terms from completed packs when applicable.
    reviewed: dict[str, str] = {}
    for filename in ("glossary.character-options.json", "glossary.actors.json"):
        path = dev_tools / "translation/generated" / filename
        if path.exists():
            reviewed.update({key: value["es"] for key, value in load(path).items() if isinstance(value, dict) and isinstance(value.get("es"), str)})

    output: dict[str, Any] = {
        "label": "Objetos mágicos",
        "mapping": {
            "description": "system.description.value",
            "activities": {"path": "system.activities", "converter": "tcoeActivitiesById"},
            "effects": {"path": "effects", "converter": "tcoeEffectsById"},
        },
        "folders": {},
        "entries": {},
    }
    for folder, value in source.get("folders", {}).items():
        output["folders"][folder] = reviewed.get(value, value)

    memory: list[dict[str, Any]] = []
    pending: list[dict[str, Any]] = []
    translated_names = 0
    translated_descriptions = 0

    for entry_id, source_entry in source.get("entries", {}).items():
        old = legacy.get("entries", {}).get(entry_id, {})
        entry: dict[str, Any] = {}
        source_name = source_entry.get("name", "")
        target_name = official.get(source_name) or reviewed.get(source_name)
        if target_name and target_name != source_name:
            entry["name"] = target_name
            translated_names += 1
            memory.append({
                "source": source_name, "target": target_name, "pack": "tcoe-magic-items",
                "documentId": entry_id, "path": "name", "confidence": 1.0,
                "sourceType": "official-pdf" if source_name in official else "reviewed-glossary",
            })
        else:
            pending.append({"entryId": entry_id, "path": "name", "source": source_name})

        # Reviewed PDF-guided HTML has priority. Legacy is retained only when
        # it genuinely differs from EN.
        source_description = source_entry.get("description", "")
        old_description = old.get("description")
        reviewed_description = reviewed_descriptions.get(entry_id)
        if isinstance(reviewed_description, str):
            entry["description"] = reviewed_description
            translated_descriptions += 1
            memory.append({
                "source": source_description, "target": reviewed_description,
                "pack": "tcoe-magic-items", "documentId": entry_id,
                "path": "description", "confidence": 1.0,
                "sourceType": "official-pdf-reviewed-html",
            })
        elif isinstance(old_description, str) and old_description != source_description:
            entry["description"] = old_description
            translated_descriptions += 1
        elif source_description.strip():
            pending.append({"entryId": entry_id, "path": "description", "sourceChars": len(source_description)})

        output["entries"][entry_id] = entry

    report = {
        "pack": "dnd-tashas-cauldron.tcoe-magic-items",
        "sourceEntries": len(source.get("entries", {})),
        "outputEntries": len(output["entries"]),
        "translatedNames": translated_names,
        "translatedDescriptions": translated_descriptions,
        "pendingFields": len(pending),
        "note": "Descriptions identical to English are intentionally omitted pending PDF-guided translation."
    }
    generated = dev_tools / "translation/generated"
    write(module_root / "compendium/dnd-tashas-cauldron.tcoe-magic-items.json", output)
    write(generated / "translation-memory.magic-items.json", memory)
    write(generated / "pending.magic-items.json", pending)
    write(generated / "report.magic-items.json", report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
