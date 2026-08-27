# 🇪🇸 D&D 5e Tasha's Cauldron of Everything -- Español (Babele)

![Foundry v13](https://img.shields.io/badge/Foundry-v13-green)![Foundry v14](https://img.shields.io/badge/Foundry-v14-green) ![dnd5e
5.3.x](https://img.shields.io/badge/dnd5e-5.3.x-blue) ![Babele
Required](https://img.shields.io/badge/Babele-required-orange) ![Tasha's
Cauldron](https://img.shields.io/badge/Tasha's%20Cauldron-required-orange)
[![Latest Release](https://img.shields.io/github/v/release/foundryvtt-sinregistrar/translate-dnd5e-tashas-cauldron?label=release)](https://github.com/foundryvtt-sinregistrar/translate-dnd5e-tashas-cauldron/releases/latest)
[![Downloads Latest Release](https://img.shields.io/github/downloads/foundryvtt-sinregistrar/translate-dnd5e-tashas-cauldron/latest/total?label=descargas%20%C3%BAltima%20release)](https://github.com/foundryvtt-sinregistrar/translate-dnd5e-tashas-cauldron/releases/latest)
[![Downloads Total](https://img.shields.io/github/downloads/foundryvtt-sinregistrar/translate-dnd5e-tashas-cauldron/total?label=descargas%20totales)](https://github.com/foundryvtt-sinregistrar/translate-dnd5e-tashas-cauldron/releases)

### Este módulo no está afiliado a Wizards of the Coast.
### Este módulo es una traducción no oficial de Tasha's Cauldron of Everything.

Este módulo contiene traducciones de contenido de **Tasha's Cauldron of Everything**, que es material propietario de Wizards of the Coast.

La traducción se ofrece de conformidad con la [Wizards of the Coast Fan Content Policy](https://dnd.wizards.com/en/digital-tools-licensing).

Dungeons & Dragons Tasha's Cauldron of Everything © Wizards of the Coast LLC. Todos los derechos reservados.

---

## 📦 Descripción
**Current version:** 1.14.0

Traducción al español de **Tasha's Cauldron of Everything** para el sistema **dnd5e** en Foundry VTT.

Implementado mediante **Babele** con arquitectura:

Mapping First → Converter Second → Normalization Layer

------------------------------------------------------------------------

## 📦 Contenido del Módulo

Este módulo proporciona traducciones estructuradas para los siete compendios de Tasha's Cauldron of Everything:

| Compendio | Estado |
|----------|:------:|
| Actores | ✅ |
| Opciones de personaje | ✅ |
| Contenido | ✅ |
| Herramientas del DM | ✅ |
| Objetos mágicos | ✅ |
| Escenas | ✅ |
| Tablas | ✅ |

------------------------------------------------------------------------

## 🧠 Arquitectura Técnica

Mapping First → Converter Second → Normalization Layer

### Convertidores

- activities
- mergeEffects
- advancementById
- journalEntryFullById
- journalPagesById
- rollTableResultsById

### Normalización

- Glosario EN→ES canónico
- Protección de macros (@UUID, &Reference, @Embed, \[\[/r ...\]\])
- Protección de tablas HTML y encabezados estructurales
- Title Case semántico en campos estructurales

------------------------------------------------------------------------

## ⚙️ Requisitos

- Foundry VTT v13
- Foundry VTT v14+
- Sistema dnd5e 5.3.x
- Babele 2.7.5+
- Módulo oficial Tasha's Cauldron of Everything 3.0.0+

------------------------------------------------------------------------

## 🚀 Instalación

### 🔹 Opción 1 — Descargar ZIP

1. Ir a la sección **Releases** del repositorio.
2. Descargar el fichero `.zip` de la última versión.
3. Descomprimir en:

	FoundryVTT/Data/modules/

4. Activar el módulo desde Foundry.
5. Activar la traducción desde Babele.

---

### 🔹 Opción 2 — Instalación directa desde Foundry (URL)

1. En Foundry, ir a **Add-on Modules → Install Module → Install from Manifest URL**.
2. Introducir la siguiente URL:

	https://raw.githubusercontent.com/foundryvtt-sinregistrar/translate-dnd5e-tashas-cauldron/main/module.json

3. Instalar el módulo.
4. Activarlo y habilitar la traducción desde Babele.

------------------------------------------------------------------------

## 📜 Licencia

Este proyecto es una traducción no oficial del contenido de Tasha's Cauldron of Everything.

Consulta la [Wizards of the Coast Fan Content Policy](https://dnd.wizards.com/en/digital-tools-licensing) para más información sobre permisos y restricciones.

---

## 📜 Changelog

Consulta: **CHANGELOG.md**

## 👤 Autor

foundryvtt-sinregistrar
