#!/usr/bin/env python3
"""Audit coverage and integrity of every distributed Tasha translation compendium."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Iterator


ROOT = Path(__file__).resolve().parents[2]
PACKS = (
    "tcoe-actors", "tcoe-character-options", "tcoe-magic-items", "tcoe-tables",
    "tcoe-content", "tcoe-dm-tools", "tcoe-scenes",
)
INTERNAL_UUID = re.compile(
    r"Compendium\.dnd-tashas-cauldron\.([^.\]]+)\."
    r"(?:JournalEntry|Item|Actor|RollTable|Scene)\.([^.\]#}\s]+)"
    r"(?:\.JournalEntryPage\.([^.\]#}\s]+))?"
)
MOJIBAKE = re.compile(r"(?:Ã.|Â.|â€|ï¿½|\ufffd)")


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def strings(value: Any, path: str = "$") -> Iterator[tuple[str, str]]:
    if isinstance(value, str):
        yield path, value
    elif isinstance(value, dict):
        for key, child in value.items():
            yield from strings(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from strings(child, f"{path}[{index}]")


def source_pages(row: dict[str, Any]) -> set[str]:
    return set(row.get("pages", {}))


def main() -> int:
    issues: list[dict[str, Any]] = []
    pack_reports: list[dict[str, Any]] = []
    sources: dict[str, dict[str, Any]] = {}
    outputs: dict[str, dict[str, Any]] = {}

    for pack in PACKS:
        source_path = ROOT / f"dev-tools/export/data/dnd-tashas-cauldron.{pack}.en.json"
        output_path = ROOT / f"compendium/dnd-tashas-cauldron.{pack}.json"
        try:
            source, output = load(source_path), load(output_path)
        except (OSError, json.JSONDecodeError) as error:
            issues.append({"type": "json-load", "pack": pack, "detail": str(error)})
            continue
        sources[pack], outputs[pack] = source, output
        source_ids, output_ids = set(source.get("entries", {})), set(output.get("entries", {}))
        missing, extra = sorted(source_ids - output_ids), sorted(output_ids - source_ids)
        if missing:
            issues.append({"type": "missing-entry-ids", "pack": pack, "ids": missing})
        if extra:
            issues.append({"type": "extra-entry-ids", "pack": pack, "ids": extra})

        missing_pages: list[dict[str, str]] = []
        extra_pages: list[dict[str, str]] = []
        if pack in {"tcoe-content", "tcoe-dm-tools"}:
            for entry_id in sorted(source_ids & output_ids):
                source_page_ids = source_pages(source["entries"][entry_id])
                output_page_ids = source_pages(output["entries"][entry_id])
                missing_pages.extend({"entryId": entry_id, "pageId": page_id} for page_id in sorted(source_page_ids - output_page_ids))
                extra_pages.extend({"entryId": entry_id, "pageId": page_id} for page_id in sorted(output_page_ids - source_page_ids))
        if missing_pages:
            issues.append({"type": "missing-page-ids", "pack": pack, "pages": missing_pages})
        if extra_pages:
            issues.append({"type": "extra-page-ids", "pack": pack, "pages": extra_pages})

        nested_field = {"tcoe-tables": "results", "tcoe-actors": "items"}.get(pack)
        source_nested = output_nested = 0
        missing_nested: list[dict[str, str]] = []
        extra_nested: list[dict[str, str]] = []
        if nested_field:
            for entry_id in sorted(source_ids & output_ids):
                source_nested_ids = set(source["entries"][entry_id].get(nested_field, {}))
                output_nested_ids = set(output["entries"][entry_id].get(nested_field, {}))
                source_nested += len(source_nested_ids)
                output_nested += len(output_nested_ids)
                missing_nested.extend({"entryId": entry_id, "id": nested_id} for nested_id in sorted(source_nested_ids - output_nested_ids))
                extra_nested.extend({"entryId": entry_id, "id": nested_id} for nested_id in sorted(output_nested_ids - source_nested_ids))
        if missing_nested:
            issues.append({"type": f"missing-{nested_field}-ids", "pack": pack, "rows": missing_nested})
        if extra_nested:
            issues.append({"type": f"extra-{nested_field}-ids", "pack": pack, "rows": extra_nested})

        mojibake = [path for path, value in strings(output) if MOJIBAKE.search(value)]
        if mojibake:
            issues.append({"type": "mojibake", "pack": pack, "paths": mojibake})
        pack_reports.append({
            "pack": f"dnd-tashas-cauldron.{pack}",
            "sourceEntries": len(source_ids),
            "outputEntries": len(output_ids),
            "missingEntries": len(missing),
            "extraEntries": len(extra),
            "missingPages": len(missing_pages),
            "extraPages": len(extra_pages),
            "nestedField": nested_field,
            "sourceNestedDocuments": source_nested,
            "outputNestedDocuments": output_nested,
            "missingNestedDocuments": len(missing_nested),
            "extraNestedDocuments": len(extra_nested),
            "mojibakeFields": len(mojibake),
        })

    checked_references = 0
    broken_references: list[dict[str, str]] = []
    for origin_pack, output in outputs.items():
        for path, value in strings(output):
            for target_pack, entry_id, page_id in INTERNAL_UUID.findall(value):
                checked_references += 1
                target_source = sources.get(target_pack)
                if not target_source or entry_id not in target_source.get("entries", {}):
                    broken_references.append({"originPack": origin_pack, "path": path, "target": f"{target_pack}/{entry_id}"})
                    continue
                if page_id and page_id not in target_source["entries"][entry_id].get("pages", {}):
                    broken_references.append({"originPack": origin_pack, "path": path, "target": f"{target_pack}/{entry_id}/{page_id}"})
    if broken_references:
        issues.append({"type": "broken-internal-references", "references": broken_references})

    pending_counts: dict[str, int] = {}
    for slug in ("content", "dm-tools", "magic-items", "tables"):
        path = ROOT / f"dev-tools/translation/generated/pending.{slug}.json"
        pending_counts[slug] = len(load(path)) if path.exists() else 0
        if pending_counts[slug]:
            issues.append({"type": "pending-fields", "pack": slug, "count": pending_counts[slug]})

    module = load(ROOT / "module.json")
    declared_paths = [row["path"] for row in module.get("languages", [])] + module.get("esmodules", [])
    missing_module_files = [path for path in declared_paths if not (ROOT / path).is_file()]
    if missing_module_files:
        issues.append({"type": "missing-module-files", "paths": missing_module_files})

    report = {
        "status": "passed" if not issues else "failed",
        "module": module.get("id"),
        "moduleVersion": module.get("version"),
        "foundryCompatibility": module.get("compatibility"),
        "packsAudited": len(pack_reports),
        "packReports": pack_reports,
        "internalReferencesChecked": checked_references,
        "brokenInternalReferences": len(broken_references),
        "pendingFields": pending_counts,
        "declaredModuleFilesChecked": len(declared_paths),
        "issues": issues,
    }
    report_path = ROOT / "dev-tools/translation/generated/report.audit-all.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not issues else 2


if __name__ == "__main__":
    raise SystemExit(main())
