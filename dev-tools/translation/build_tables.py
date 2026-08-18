#!/usr/bin/env python3
"""Build the Babele RollTable translation and a range-aligned review queue."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


PROTECTED = re.compile(r"@(?:UUID|Embed)\[([^\]]+)\]|(?:&|&amp;)Reference\[([^\]]+)\]|\[\[([^\]]+)\]\]")


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def tokens(value: str) -> Counter[str]:
    return Counter(next(part for part in match if part is not None) for match in PROTECTED.findall(value or ""))


def range_key(value: Any) -> str:
    return "-".join(str(number) for number in value) if isinstance(value, list) else ""


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    source = load(root / "dev-tools/export/data/dnd-tashas-cauldron.tcoe-tables.en.json")
    legacy = load(root / "dev-tools/export/_data/dnd-tashas-cauldron.tcoe-tables.json")
    reviewed_path = root / "dev-tools/translation/reviewed-tables.json"
    reviewed = load(reviewed_path) if reviewed_path.exists() else {}

    output: dict[str, Any] = {
        "label": "Tablas de Tasha",
        "mapping": {
            "description": "description",
            "results": {"path": "results", "converter": "tcoeTableResultsById"},
        },
        "folders": {},
        "entries": {},
    }
    pending: list[dict[str, Any]] = []
    alignment_warnings: list[dict[str, Any]] = []
    token_issues: list[dict[str, Any]] = []

    for folder in source.get("folders", {}):
        translated = reviewed.get("folders", {}).get(folder)
        if translated:
            output["folders"][folder] = translated
        else:
            output["folders"][folder] = folder
            pending.append({"path": f"folders.{folder}", "source": folder})

    for entry_id, entry in source.get("entries", {}).items():
        legacy_entry = legacy.get("entries", {}).get(entry_id, {})
        patch = reviewed.get("entries", {}).get(entry_id, {})
        target: dict[str, Any] = {}
        for field in ("name", "description"):
            translated = patch.get(field)
            if isinstance(translated, str) and translated:
                target[field] = translated
                if tokens(entry.get(field, "")) != tokens(translated):
                    token_issues.append({"entryId": entry_id, "path": field})
            elif entry.get(field):
                pending.append({"entryId": entry_id, "path": field, "source": entry[field]})

        old_results = legacy_entry.get("results", {}) if isinstance(legacy_entry, dict) else {}
        reviewed_results = patch.get("results", {}) if isinstance(patch, dict) else {}
        translated_results: dict[str, Any] = {}
        for result_id, result in entry.get("results", {}).items():
            key = range_key(result.get("range"))
            old_text = old_results.get(key)
            if old_text is None:
                alignment_warnings.append({"entryId": entry_id, "resultId": result_id, "range": key})
            translated = reviewed_results.get(result_id)
            if isinstance(translated, str) and translated:
                translated_results[result_id] = {"text": translated}
                if tokens(result.get("text", "")) != tokens(translated):
                    token_issues.append({"entryId": entry_id, "path": f"results.{result_id}.text"})
            elif result.get("text"):
                pending.append({
                    "entryId": entry_id,
                    "resultId": result_id,
                    "range": key,
                    "path": f"results.{result_id}.text",
                    "source": result["text"],
                    "legacySource": old_text,
                })
        if translated_results:
            target["results"] = translated_results
        output["entries"][entry_id] = target

    generated = root / "dev-tools/translation/generated"
    report = {
        "pack": "dnd-tashas-cauldron.tcoe-tables",
        "sourceEntries": len(source.get("entries", {})),
        "outputEntries": len(output["entries"]),
        "sourceResults": sum(len(row.get("results", {})) for row in source.get("entries", {}).values()),
        "translatedFields": sum(bool(row.get("name")) + bool(row.get("description")) + len(row.get("results", {})) for row in output["entries"].values()),
        "pendingFields": len(pending),
        "legacyAlignmentWarnings": len(alignment_warnings),
        "protectedTokenIssues": len(token_issues),
    }
    write(root / "compendium/dnd-tashas-cauldron.tcoe-tables.json", output)
    write(generated / "pending.tables.json", pending)
    write(generated / "alignment-warnings.tables.json", alignment_warnings)
    write(generated / "protected-token-issues.tables.json", token_issues)
    write(generated / "report.tables.json", report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 2 if token_issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
