#!/usr/bin/env python3
"""Generate the reviewed Spanish magic-item overview from validated item names."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "dev-tools/export/data/dnd-tashas-cauldron.tcoe-content.en.json"
ITEMS = ROOT / "compendium/dnd-tashas-cauldron.tcoe-magic-items.json"
OUTPUT = ROOT / "dev-tools/translation/reviewed-content.batch-30.json"
ENTRY_ID = "tcoeMagicItems00"
PAGE_ID = "yYCrYxuC86LQSwoO"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def main() -> int:
    source = load(SOURCE)["entries"][ENTRY_ID]["pages"][PAGE_ID]["text"]
    translated_items = load(ITEMS)["entries"]

    def translate_label(match: re.Match[str]) -> str:
        item_id, original = match.groups()
        translated = translated_items.get(item_id, {}).get("name")
        if not translated:
            raise KeyError(f"Missing translated magic-item name: {item_id} ({original})")
        return f"@UUID[Compendium.dnd-tashas-cauldron.tcoe-magic-items.Item.{item_id}]{{{translated}}}"

    text = re.sub(
        r"@UUID\[Compendium\.dnd-tashas-cauldron\.tcoe-magic-items\.Item\.([^\]]+)\]\{([^}]*)\}",
        translate_label,
        source,
    )
    replacements = {
        "<p>This section presents magic items that can be introduced into any campaign. Here you’ll find items of all rarities, including artifacts. Magic spellcasting focuses for every spellcasting class are also available here. And some of the items in this section represent a new type of wondrous item: magic tattoos.</p>": "<p>Esta sección presenta objetos mágicos que pueden introducirse en cualquier campaña. Aquí encontrarás objetos de todas las rarezas, incluidos artefactos. También se ofrecen canalizadores mágicos para todas las clases lanzadoras de conjuros. Además, algunos objetos de esta sección representan un nuevo tipo de objeto maravilloso: los tatuajes mágicos.</p>",
        "<p>The Magic Items table lists all the magic items in this chapter and notes the rarity of each one. The table also indicates whether an item requires attunement. All the items use the magic items rules in the Dungeon Master’s Guide.</p>": "<p>La tabla Objetos mágicos enumera todos los objetos mágicos de este capítulo e indica la rareza de cada uno. También señala si requieren sintonización. Todos emplean las reglas de objetos mágicos de la Guía del Dungeon Master.</p>",
        "<caption>Magic Items by Rarity</caption>": "<caption>Objetos mágicos por rareza</caption>",
        "<th>Rarity</th>": "<th>Rareza</th>",
        "<th>Item</th>": "<th>Objeto</th>",
        "<th>Attunement</th>": "<th>Sintonización</th>",
        "<td>Common</td>": "<td>Común</td>",
        "<td>Common+</td>": "<td>Común+</td>",
        "<td>Uncommon</td>": "<td>Infrecuente</td>",
        "<td>Uncommon+</td>": "<td>Infrecuente+</td>",
        "<td>Rare</td>": "<td>Raro</td>",
        "<td>Rare+</td>": "<td>Raro+</td>",
        "<td>Very Rare</td>": "<td>Muy raro</td>",
        "<td>Legendary</td>": "<td>Legendario</td>",
        "<td>Artifact</td>": "<td>Artefacto</td>",
        "<td>Varies</td>": "<td>Variable</td>",
        "<td>Yes</td>": "<td>Sí</td>",
        "<td>No</td>": "<td>No</td>",
    }
    for original, translated in replacements.items():
        text = text.replace(original, translated)

    remaining = re.findall(r">(?:Common|Uncommon|Rare|Very Rare|Legendary|Artifact|Varies|Yes)<", text)
    if remaining:
        raise ValueError(f"Untranslated table vocabulary remains: {remaining}")

    payload = {"entries": {ENTRY_ID: {"pages": {PAGE_ID: {"text": text}}}}}
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT.name} with {text.count('@UUID[')} translated item references")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
