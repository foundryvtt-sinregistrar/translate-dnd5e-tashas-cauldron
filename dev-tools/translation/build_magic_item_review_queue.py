#!/usr/bin/env python3
"""Build a bilingual review queue for PDF-guided magic-item descriptions."""

from __future__ import annotations

import html
import json
import re
from pathlib import Path
from typing import Any


MACRO = re.compile(r"@(?:UUID|Embed)\[[^\]]+\](?:\{[^}]*\})?|&Reference\[[^\]]+\](?:\{[^}]*\})?|\[\[[^\]]+\]\]")


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_spanish(value: str) -> str:
    value = re.sub(r"\s+\+[123]$", "", value)
    return re.sub(r"\s+(ligero|medio|pesado)$", "", value, flags=re.IGNORECASE)


def strip_html(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", html.unescape(value)).strip()


def main() -> int:
    module_root = Path(__file__).resolve().parents[2]
    dev_tools = module_root / "dev-tools"
    source = load(dev_tools / "export/data/dnd-tashas-cauldron.tcoe-magic-items.en.json")
    official = load(dev_tools / "translation/official-magic-item-names.json")
    sections = load(dev_tools / "export/_data/extracted/magic-item-pdf-sections.es.json")

    queue: list[dict[str, Any]] = []
    missing: list[dict[str, str]] = []
    counts = {"simple": 0, "structured": 0, "layout-review": 0}
    known_bad = {
        "Crónica cristalina",
        "Incensario de devoto",
        "Mortero y Maja de Baba Yaga",
        "Tratado fulminante",
    }
    for entry_id, entry in source.get("entries", {}).items():
        english_name = entry.get("name", "")
        spanish_name = official.get(english_name)
        if not spanish_name:
            continue
        heading = canonical_spanish(spanish_name)
        section = sections.get(heading)
        if not section:
            missing.append({"entryId": entry_id, "englishName": english_name, "spanishName": spanish_name})
            continue

        spanish_text = section["text"]
        span = section["source"]["lastPart"] - section["source"]["firstPart"]
        begins_cleanly = bool(re.match(r"^(Objeto maravilloso|Arma \(|Arma,|Armadura)", spanish_text, re.IGNORECASE))
        has_table_signals = bool(re.search(r"\b(?:d4|d6|d8|d10|d12|d20|d100)\b", spanish_text, re.IGNORECASE))
        if heading in known_bad or not begins_cleanly:
            complexity = "layout-review"
        elif span > 0 or has_table_signals or "<table" in entry.get("description", ""):
            complexity = "structured"
        else:
            complexity = "simple"
        counts[complexity] += 1

        description = entry.get("description", "")
        queue.append({
            "entryId": entry_id,
            "englishName": english_name,
            "spanishName": spanish_name,
            "complexity": complexity,
            "source": section["source"],
            "protectedMacros": MACRO.findall(description),
            "english": {
                "html": description,
                "text": strip_html(description),
            },
            "spanishPdf": {
                "text": spanish_text,
                "lines": section["lines"],
            },
            "status": "pending-html-reconstruction",
        })

    generated = dev_tools / "translation/generated"
    generated.mkdir(parents=True, exist_ok=True)
    (generated / "review-queue.magic-items.json").write_text(
        json.dumps(queue, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    report = {
        "queueEntries": len(queue),
        "complexity": counts,
        "missingPdfSections": missing,
        "policy": "Do not copy spanishPdf.text directly into compendium HTML; reconstruct and verify protectedMacros first.",
    }
    (generated / "report.magic-item-review-queue.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
