#!/usr/bin/env python3
"""Build the Tasha journal translation with current Foundry page IDs."""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


PROTECTED = re.compile(r"@(?:UUID|Embed)\[([^\]]+)\]|(?:&|&amp;)Reference\[([^\]]+)\]|\[\[([^\]]+)\]\]")


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def deep_merge(target: dict[str, Any], patch: dict[str, Any]) -> dict[str, Any]:
    for key, value in patch.items():
        if isinstance(value, dict) and isinstance(target.get(key), dict):
            deep_merge(target[key], value)
        else:
            target[key] = value
    return target


def tokens(value: str) -> Counter[str]:
    return Counter(next(part for part in match if part is not None) for match in PROTECTED.findall(value or ""))


def translation_memory(generated: Path) -> tuple[dict[str, str], list[dict[str, Any]]]:
    candidates: dict[str, set[str]] = defaultdict(set)
    for path in sorted(generated.glob("translation-memory.*.json")):
        for pair in load(path):
            source, target = pair.get("source"), pair.get("target")
            if isinstance(source, str) and source and isinstance(target, str) and target:
                candidates[source].add(target)
    conflicts = [
        {"source": source, "targets": sorted(targets)}
        for source, targets in candidates.items() if len(targets) > 1
    ]
    return {source: next(iter(targets)) for source, targets in candidates.items() if len(targets) == 1}, conflicts


def build_pack(pack_name: str, slug: str, label: str) -> int:
    root = Path(__file__).resolve().parents[2]
    generated = root / "dev-tools/translation/generated"
    source = load(root / f"dev-tools/export/data/dnd-tashas-cauldron.{pack_name}.en.json")
    legacy = load(root / f"dev-tools/export/_data/dnd-tashas-cauldron.{pack_name}.json")
    reviewed: dict[str, Any] = {"folders": {}, "entries": {}}
    for reviewed_path in sorted((root / "dev-tools/translation").glob(f"reviewed-{slug}*.json")):
        deep_merge(reviewed, load(reviewed_path))
    terms_path = root / f"dev-tools/translation/official-{slug}-terms.json"
    official_terms = load(terms_path) if terms_path.exists() else {}
    memory, memory_conflicts = translation_memory(generated)
    relevant_sources = set(source.get("folders", {}))
    for entry in source.get("entries", {}).values():
        relevant_sources.update(value for value in (entry.get("name"), entry.get("folder")) if value)
        for page in entry.get("pages", {}).values():
            relevant_sources.update(value for value in (page.get("name"), page.get("text")) if value)
    relevant_memory_conflicts = [
        row for row in memory_conflicts
        if row["source"] in relevant_sources and row["source"] not in official_terms
    ]

    output: dict[str, Any] = {
        "label": label,
        "mapping": {"pages": {"path": "pages", "converter": "tcoeJournalPagesById"}},
        "folders": {},
        "entries": {},
    }
    pending: list[dict[str, Any]] = []
    alignment: list[dict[str, Any]] = []
    token_issues: list[dict[str, Any]] = []
    memory_hits = 0

    for folder in source.get("folders", {}):
        translated = reviewed.get("folders", {}).get(folder) or official_terms.get(folder) or memory.get(folder)
        output["folders"][folder] = translated or folder
        if translated: memory_hits += int(folder in memory and folder not in reviewed.get("folders", {}))
        else: pending.append({"path": f"folders.{folder}", "source": folder})

    for entry_id, entry in source.get("entries", {}).items():
        patch = reviewed.get("entries", {}).get(entry_id, {})
        target: dict[str, Any] = {}
        for field in ("name", "folder"):
            original = entry.get(field, "")
            translated = patch.get(field) or official_terms.get(original) or memory.get(original)
            if translated:
                target[field] = translated
                memory_hits += int(original in memory and field not in patch)
            elif original:
                pending.append({"entryId": entry_id, "path": field, "source": original})

        legacy_pages = legacy.get("entries", {}).get(entry_id, {}).get("pages", {})
        legacy_names = {row.get("name", key) for key, row in legacy_pages.items()}
        translated_pages: dict[str, Any] = {}
        reviewed_pages = patch.get("pages", {})
        for page_id, page in entry.get("pages", {}).items():
            page_patch = reviewed_pages.get(page_id, {})
            page_target: dict[str, str] = {}
            for field in ("name", "text"):
                original = page.get(field, "")
                translated = page_patch.get(field) or official_terms.get(original) or memory.get(original)
                if translated:
                    page_target[field] = translated
                    memory_hits += int(original in memory and field not in page_patch)
                    if tokens(original) != tokens(translated):
                        token_issues.append({"entryId": entry_id, "pageId": page_id, "path": field})
                elif original:
                    pending.append({"entryId": entry_id, "pageId": page_id, "pageName": page.get("name"), "path": field, "source": original})
            if page_target:
                translated_pages[page_id] = page_target
            if page.get("name") not in legacy_names:
                alignment.append({"entryId": entry_id, "pageId": page_id, "pageName": page.get("name")})
        if translated_pages: target["pages"] = translated_pages
        output["entries"][entry_id] = target

    report = {
        "pack": f"dnd-tashas-cauldron.{pack_name}",
        "sourceEntries": len(source.get("entries", {})),
        "sourcePages": sum(len(row.get("pages", {})) for row in source.get("entries", {}).values()),
        "outputEntries": len(output["entries"]),
        "translatedPages": sum(len(row.get("pages", {})) for row in output["entries"].values()),
        "translationMemoryHits": memory_hits,
        "pendingFields": len(pending),
        "alignmentWarnings": len(alignment),
        "translationMemoryConflicts": len(relevant_memory_conflicts),
        "protectedTokenIssues": len(token_issues),
    }
    write(root / f"compendium/dnd-tashas-cauldron.{pack_name}.json", output)
    write(generated / f"pending.{slug}.json", pending)
    write(generated / f"alignment-warnings.{slug}.json", alignment)
    write(generated / f"conflicts.{slug}.json", relevant_memory_conflicts)
    write(generated / f"protected-token-issues.{slug}.json", token_issues)
    write(generated / f"report.{slug}.json", report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 2 if token_issues or alignment else 0


def main() -> int:
    return build_pack("tcoe-content", "content", "El Caldero de Tasha para Todo")


if __name__ == "__main__":
    raise SystemExit(main())
