# 🇬🇧 D&D 5e Tasha's Cauldron of Everything -- Spanish (Babele)

![Foundry v14](https://img.shields.io/badge/Foundry-v14-green) ![dnd5e
5.3.x](https://img.shields.io/badge/dnd5e-5.3.x-blue) ![Babele
Required](https://img.shields.io/badge/Babele-required-orange) ![Tasha's
Cauldron](https://img.shields.io/badge/Tasha's%20Cauldron-required-orange)
[![Latest Release](https://img.shields.io/github/v/release/foundryvtt-sinregistrar/translate-dnd5e-tashas-cauldron?label=release)](https://github.com/foundryvtt-sinregistrar/translate-dnd5e-tashas-cauldron/releases/latest)
[![Downloads Latest Release](https://img.shields.io/github/downloads/foundryvtt-sinregistrar/translate-dnd5e-tashas-cauldron/latest/total?label=downloads%20latest%20release)](https://github.com/foundryvtt-sinregistrar/translate-dnd5e-tashas-cauldron/releases/latest)
[![Downloads Total](https://img.shields.io/github/downloads/foundryvtt-sinregistrar/translate-dnd5e-tashas-cauldron/total?label=total%20downloads)](https://github.com/foundryvtt-sinregistrar/translate-dnd5e-tashas-cauldron/releases)

### This module is not affiliated with Wizards of the Coast.
### This module is an unofficial Spanish translation of Tasha's Cauldron of Everything.

This module contains translations of content from **Tasha's Cauldron of Everything**, which is proprietary material of Wizards of the Coast.

The translation is offered in compliance with the [Wizards of the Coast Fan Content Policy](https://dnd.wizards.com/en/digital-tools-licensing).

Dungeons & Dragons Tasha's Cauldron of Everything © Wizards of the Coast LLC. All rights reserved.

---

## 📦 Description
**Current version:** 1.14.0

Spanish translation of **Tasha's Cauldron of Everything** for the **dnd5e** system in Foundry VTT.

Implemented using **Babele** with architecture:

Mapping First → Converter Second → Normalization Layer

------------------------------------------------------------------------

## 📦 Module Content

This module provides structured translations for the seven Tasha's Cauldron of Everything compendiums:

| Compendium | Status |
|-----------|:------:|
| Actors | ✅ |
| Character Options | ✅ |
| Content | ✅ |
| DM Tools | ✅ |
| Magic Items | ✅ |
| Scenes | ✅ |
| Tables | ✅ |

------------------------------------------------------------------------

## 🧠 Technical Architecture

Mapping First → Converter Second → Normalization Layer

### Converters

- activities
- mergeEffects
- advancementById
- journalEntryFullById
- journalPagesById
- rollTableResultsById

### Normalization

- Canonical EN→ES glossary
- Macro protection (@UUID, &Reference, @Embed, \[\[/r ...\]\])
- HTML table and structural heading protection
- Semantic Title Case in structural fields

------------------------------------------------------------------------

## ⚙️ Requirements

- Foundry VTT v13
- Foundry VTT v14+
- dnd5e 5.3.x
- Babele 2.7.5+
- Tasha's Cauldron of Everything 3.0.0+

------------------------------------------------------------------------

## 🚀 Installation

### 🔹 Option 1 — Download ZIP

1. Go to the **Releases** section of the repository.
2. Download the `.zip` file of the latest version.
3. Extract to:

	FoundryVTT/Data/modules/

4. Activate the module from Foundry.
5. Enable the translation from Babele.

---

### 🔹 Option 2 — Direct installation from Foundry (URL)

1. In Foundry, go to **Add-on Modules → Install Module → Install from Manifest URL**.
2. Enter the following URL:

	https://raw.githubusercontent.com/foundryvtt-sinregistrar/translate-dnd5e-tashas-cauldron/main/module.json

3. Install the module.
4. Activate it and enable the translation from Babele.

------------------------------------------------------------------------

## 📜 License

This project is an unofficial translation of content from Tasha's Cauldron of Everything.

Consult the [Wizards of the Coast Fan Content Policy](https://dnd.wizards.com/en/digital-tools-licensing) for more information on permissions and restrictions.

---

## 📜 Changelog

See: **CHANGELOG.md**

## 👤 Author

foundryvtt-sinregistrar
