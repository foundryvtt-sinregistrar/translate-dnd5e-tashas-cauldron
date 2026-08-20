#!/usr/bin/env python3
"""Extract the complete source-attributed Spanish corpus from the split book PDF."""

from __future__ import annotations

import json
import re
from pathlib import Path

from pypdf import PdfReader


def clean(value: str) -> str:
    value = value.replace("\u00ad", "").replace("�", "")
    return re.sub(r"[ \t]+", " ", value).strip()


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    pdf_dir = root / "dev-tools/export/_data/pdf"
    output = root / "dev-tools/export/_data/extracted/tashas-pdf-corpus.es.json"
    report_path = root / "dev-tools/translation/generated/report.pdf-corpus.json"
    rows = []
    empty_parts = []
    for part in range(1, 192):
        path = pdf_dir / f"dnd-tashas-cauldron_Part_{part}.pdf"
        reader = PdfReader(str(path))
        lines = []
        for page_number, page in enumerate(reader.pages, start=1):
            for line_number, raw in enumerate((page.extract_text() or "").splitlines(), start=1):
                text = clean(raw)
                if text:
                    lines.append({"page": page_number, "line": line_number, "text": text})
        if not lines: empty_parts.append(part)
        rows.append({"part": part, "file": path.name, "lines": lines, "text": "\n".join(row["text"] for row in lines)})
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = {
        "pdfParts": len(rows),
        "partsWithText": sum(bool(row["lines"]) for row in rows),
        "emptyParts": empty_parts,
        "lines": sum(len(row["lines"]) for row in rows),
        "characters": sum(len(row["text"]) for row in rows),
        "firstTextPart": next((row["part"] for row in rows if row["lines"]), None),
        "lastTextPart": next((row["part"] for row in reversed(rows) if row["lines"]), None),
    }
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
