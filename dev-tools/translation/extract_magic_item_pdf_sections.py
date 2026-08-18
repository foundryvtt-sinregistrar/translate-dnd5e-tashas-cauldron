#!/usr/bin/env python3
"""Extract source-attributed Spanish magic-item sections from PDF parts 117-135."""

from __future__ import annotations

import json
import re
import unicodedata
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

from pypdf import PdfReader


FIRST_PART = 117
LAST_PART = 135


def normalize(value: str) -> str:
    value = unicodedata.normalize("NFKD", value.upper())
    value = "".join(char for char in value if not unicodedata.combining(char))
    value = value.replace("0", "O").replace("1", "I")
    return re.sub(r"[^A-Z0-9]+", " ", value).strip()


def clean_line(value: str) -> str:
    value = value.replace("\u00ad", "").replace("�", "")
    return re.sub(r"[ \t]+", " ", value).strip()


def is_noise(value: str) -> bool:
    normalized = normalize(value)
    return (
        not normalized
        or bool(re.match(r"^CAPITULO 3 .* MISCELANEA MAGICA(?: \d+)?$", normalized))
        or bool(re.match(r"^\d+ CAPITULO 3", normalized))
        or normalized in {"DESCRIPCIONES DE OBJETOS MAGICOS", "OBJETOS MAGICOS"}
    )


def best_heading(line: str, headings: list[str]) -> tuple[str | None, float]:
    candidate = normalize(line)
    if not candidate or len(candidate) < 5 or len(candidate) > 70:
        return None, 0.0
    best = max(headings, key=lambda heading: SequenceMatcher(None, candidate, normalize(heading)).ratio())
    score = SequenceMatcher(None, candidate, normalize(best)).ratio()
    return (best, score) if score >= 0.78 else (None, score)


def main() -> int:
    module_root = Path(__file__).resolve().parents[2]
    pdf_dir = module_root / "dev-tools/export/_data/pdf"
    names_path = module_root / "dev-tools/translation/official-magic-item-names.json"
    output_path = module_root / "dev-tools/export/_data/extracted/magic-item-pdf-sections.es.json"
    report_path = module_root / "dev-tools/translation/generated/report.magic-item-pdf-extraction.json"

    official: dict[str, str] = json.loads(names_path.read_text(encoding="utf-8"))
    # Variant rows share a single description in the book; segment only canonical headings.
    spanish_to_english: dict[str, list[str]] = {}
    for english, spanish in official.items():
        canonical = re.sub(r"\s+\+[123]$", "", spanish)
        canonical = re.sub(r"\s+(ligero|medio|pesado)$", "", canonical, flags=re.IGNORECASE)
        spanish_to_english.setdefault(canonical, []).append(english)
    headings = sorted(spanish_to_english, key=len, reverse=True)

    rows: list[dict[str, Any]] = []
    for part in range(FIRST_PART, LAST_PART + 1):
        path = pdf_dir / f"dnd-tashas-cauldron_Part_{part}.pdf"
        reader = PdfReader(str(path))
        for page_number, page in enumerate(reader.pages, start=1):
            for line_number, raw in enumerate((page.extract_text() or "").splitlines(), start=1):
                line = clean_line(raw)
                if line and not is_noise(line):
                    rows.append({"part": part, "page": page_number, "line": line_number, "text": line})

    hits: list[dict[str, Any]] = []
    last_heading = None
    for index, row in enumerate(rows):
        heading, score = best_heading(row["text"], headings)
        if not heading or heading == last_heading:
            continue
        # Headings are predominantly uppercase; avoid matching prose fragments.
        letters = [char for char in row["text"] if char.isalpha()]
        uppercase_ratio = sum(char.isupper() for char in letters) / len(letters) if letters else 0
        if uppercase_ratio < 0.72:
            continue
        hits.append({"index": index, "heading": heading, "score": round(score, 3), **row})
        last_heading = heading

    sections: dict[str, Any] = {}
    for position, hit in enumerate(hits):
        end = hits[position + 1]["index"] if position + 1 < len(hits) else len(rows)
        body = [row for row in rows[hit["index"] + 1:end] if not is_noise(row["text"])]
        sections[hit["heading"]] = {
            "englishNames": spanish_to_english[hit["heading"]],
            "source": {
                "firstPart": hit["part"],
                "lastPart": body[-1]["part"] if body else hit["part"],
                "headingScore": hit["score"],
            },
            "lines": [row["text"] for row in body],
            "text": "\n".join(row["text"] for row in body),
        }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(sections, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = {
        "pdfParts": [FIRST_PART, LAST_PART],
        "candidateCanonicalHeadings": len(headings),
        "extractedSections": len(sections),
        "missingHeadings": sorted(set(headings) - set(sections)),
        "sections": {
            heading: {
                "source": value["source"],
                "characters": len(value["text"]),
                "lines": len(value["lines"]),
            }
            for heading, value in sections.items()
        },
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: report[key] for key in ("candidateCanonicalHeadings", "extractedSections", "missingHeadings")}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
