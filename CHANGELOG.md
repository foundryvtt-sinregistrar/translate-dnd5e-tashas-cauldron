# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Changed
- Updated compatibility for Foundry VTT 14.368, dnd5e 6.0.3, Babele 2.9.1, and Tasha's Cauldron of Everything 4.0.0.

### Fixed
- Register compendiums and converters through `babele.init`, deferring language lookup until `setup` when core settings are available.
- Use the configured Babele session language and register only for Spanish and its regional variants.

### Added
- Regression tests for initialization timing, configured language selection, and converter coverage across all seven compendiums.

---

## [1.14.0] - 2026-08-26

### Added
- Initial Foundry VTT module structure and Babele integration.
- Export workflow for the seven Tasha's Cauldron compendiums.
- ID-based converters and normalization for actors, content, journals, scenes, tables, and items.
- Spanish translations for character options, actors, magic items, tables, content, DM tools, and puzzle scenes.

### Changed
- Completed the Spanish localization of compendium names, folders, rules, classes, patrons, puzzles, and reference material.
- Added PDF-guided translation and review workflows for structured content.
- Added release archive exclusions through `.gitattributes`.
- Updated Foundry VTT, dnd5e, Babele, and official module compatibility metadata.
- Replaced the short license file with the complete Apache 2.0 license in `LICENSE.md`.

### Fixed
- Resolved Tasha content terminology conflicts.
- Validated case-insensitive Foundry references.
- Corrected puzzle mechanics, table tokens, and structured embedded descriptions during review.
- Added full compendium audits and final translation coverage reports.
