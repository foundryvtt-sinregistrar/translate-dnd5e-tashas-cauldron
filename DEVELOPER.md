# Developer Documentation

## Design goals

- Preserve original document IDs and structure.
- Preserve Foundry macros, UUIDs, embeds, and inline rolls.
- Use mapping-first and converter-second translations.
- Keep every source compendium in a separate JSON file under `compendium/`.

## Source extraction

See `dev-tools/export/README.md`. The browser-console exporter reads all seven
official packs through Foundry's document API and produces English reference
JSON while preserving stable document IDs.
