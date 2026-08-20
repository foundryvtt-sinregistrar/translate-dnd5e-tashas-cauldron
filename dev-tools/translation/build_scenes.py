#!/usr/bin/env python3
"""Build and validate the two translated Tasha puzzle scenes."""

from __future__ import annotations

import json
from pathlib import Path


TRANSLATIONS = {
    "folders": {"Puzzles": "Rompecabezas"},
    "entries": {
        "tcoeFourByFour00": {"name": "Cuatro por cuatro"},
        "tcoeRecklessStep": {"name": "Pasos temerarios"},
    },
}


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    source = json.loads((root / "dev-tools/export/data/dnd-tashas-cauldron.tcoe-scenes.en.json").read_text(encoding="utf-8-sig"))
    output = {
        "label": "Escenas",
        "mapping": {"navigation": "navName"},
        "folders": TRANSLATIONS["folders"],
        "entries": TRANSLATIONS["entries"],
    }
    source_ids = set(source.get("entries", {}))
    output_ids = set(output["entries"])
    missing = sorted(source_ids - output_ids)
    extra = sorted(output_ids - source_ids)
    report = {
        "pack": "dnd-tashas-cauldron.tcoe-scenes",
        "sourceEntries": len(source_ids),
        "outputEntries": len(output_ids),
        "translatedFolders": len(output["folders"]),
        "missingEntries": missing,
        "extraEntries": extra,
        "sourceNotes": sum(len(row.get("notes", {})) for row in source.get("entries", {}).values()),
    }
    (root / "compendium/dnd-tashas-cauldron.tcoe-scenes.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report_path = root / "dev-tools/translation/generated/report.scenes.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 2 if missing or extra else 0


if __name__ == "__main__":
    raise SystemExit(main())
