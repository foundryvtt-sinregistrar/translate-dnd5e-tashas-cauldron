# Informe de contenido en inglés — Tasha

Fecha: 2026-09-21. Rama: `feature/dnd5e-6.0.3`. Revisión sobre los archivos locales posteriores al commit `0844820`.

## Estado de la corrección — 2026-09-21

**Corregidos los 19 hallazgos confirmados (ING-01 a ING-19).** Se han actualizado los cuatro compendios afectados, las dos memorias de traducción y el lote de contenido correspondiente. Las correcciones revisadas se guardan en `dev-tools/translation/reviewed-english-cleanup.json` y se aplican desde los generadores para evitar regresiones.

Validación realizada:

- Exactamente 19 valores de los compendios modificados respecto al commit `0844820`, sin cambios de claves, HTML, UUID, macros ni tiradas.
- Regeneración de actores, opciones de personaje, objetos mágicos y contenido en una copia temporal: los 19 valores corregidos coinciden con los distribuidos.
- Auditoría de los siete compendios sin incidencias y 11 pruebas de registro superadas.
- Se mantienen los términos necesarios para los rompecabezas, los nombres propios y las fuentes inglesas.

La armonización editorial de topónimos, marcas y metadatos se mantiene separada de estas correcciones. Falta la comprobación visual dentro de Foundry. Las evidencias inglesas y el inventario siguientes documentan la revisión inicial; no representan pendientes actuales.

## Resultado de la revisión inicial

Se han identificado **19 campos con contenido pendiente de traducir en los compendios distribuidos**: 4 en actores, 5 en opciones de personaje, 2 en contenido y 8 valores de carpetas de objetos mágicos. Un campo puede contener varios nombres o párrafos ingleses. Hay además referencias editoriales que conviene armonizar y metadatos de presentación en inglés.

Se analizaron **125 archivos JSON**, con **64,645 valores de texto**. Todos se pudieron interpretar como JSON. El inventario completo figura al final y corresponde al estado anterior a las correcciones.

## Alcance y método

- Recorrido recursivo de todos los JSON del módulo, incluidos archivos auxiliares y exportaciones ignoradas por Git. Se excluyen `.git` y los dos JSON temporales producidos exclusivamente para esta revisión.
- Comparación de los siete compendios con `dev-tools/export/data/*.en.json`, tanto de campos completos como de fragmentos dentro del HTML.
- Búsqueda de vocabulario inglés y de nombres presentes en las fuentes, con revisión contextual de las coincidencias. Se examinan también etiquetas visibles `{texto}` de enlaces UUID.
- Distinción entre texto visible y claves técnicas, rutas, macros, identificadores, nombres propios y material fuente deliberadamente inglés.
- Es una revisión estática con detección heurística y revisión de candidatos; no una garantía de ausencia absoluta de anglicismos ni una comprobación del contenido nuevo del módulo oficial 4.0.0 en ejecución. Las exportaciones guardadas pueden ser anteriores a esa versión.

## Hallazgos confirmados

### ING-01. Lista de conjuros del caballero de la muerte

Estado: **Corregido**.

- Prioridad: **Alta**.
- Archivo: `compendium/dnd-tashas-cauldron.tcoe-actors.json` (línea 2419).
- Campo: `$.entries.tcoeDeathKnight0.items.DoaZn93hetq3H5UW.description`.
- Inglés detectado: command, compelled duel, searing smite; hold person, magic weapon; dispel magic, elemental weapon; banishment, staggering smite; destructive wave (necrotic).
- Corrección recomendada: Traducir los diez nombres de conjuros y el tipo de daño. El texto está en una sección secreta, visible para el DJ.

### ING-02. Encabezado de ayuda del flumph

Estado: **Corregido**.

- Prioridad: **Media**.
- Archivo: `compendium/dnd-tashas-cauldron.tcoe-actors.json` (línea 2806).
- Campo: `$.entries.tcoeFlumph000000.items.IolQj4vA4MeO1syv.description`.
- Inglés detectado: Foundry Tip:
- Corrección recomendada: Sustituir por "Consejo de Foundry:".

### ING-03. Nota de la reflexión

Estado: **Corregido**.

- Prioridad: **Media**.
- Archivo: `compendium/dnd-tashas-cauldron.tcoe-actors.json` (línea 3373).
- Campo: `$.entries.tcoeReflection00.biography`.
- Inglés detectado: Foundry Note
- Corrección recomendada: Sustituir por "Nota de Foundry".

### ING-04. Nota y referencia al rasgo

Estado: **Corregido**.

- Prioridad: **Media**.
- Archivo: `compendium/dnd-tashas-cauldron.tcoe-actors.json` (línea 3408).
- Campo: `$.entries.tcoeShadowDespai.items.bNuEiPi9nNIGIN1w.description`.
- Inglés detectado: Foundry Note; Weight of Sorrow
- Corrección recomendada: Traducir el encabezado y la mención del rasgo, alineándola con el nombre español del documento.

### ING-05. Dote de telepatía

Estado: **Corregido**.

- Prioridad: **Alta**.
- Archivo: `compendium/dnd-tashas-cauldron.tcoe-character-options.json` (línea 1644).
- Campo: `$.entries.tcoeFeatTelepath.description`.
- Inglés detectado: {detect thoughts}; Detect Thoughts
- Corrección recomendada: Traducir la etiqueta visible del enlace y el nombre de actividad citado en las instrucciones; conservar el UUID.

### ING-06. Compañero primigenio

Estado: **Corregido**.

- Prioridad: **Alta**.
- Archivo: `compendium/dnd-tashas-cauldron.tcoe-character-options.json` (línea 2507).
- Campo: `$.entries.tcoePrimalCompan.description`.
- Inglés detectado: Beast of the Land; Beast of the Sea; Beast of the Sky
- Corrección recomendada: Traducir las tres etiquetas visibles de los enlaces sin modificar sus UUID.

### ING-07. Condición del escudo de repulsión

Estado: **Corregido**.

- Prioridad: **Alta**.
- Archivo: `compendium/dnd-tashas-cauldron.tcoe-character-options.json` (línea 2773).
- Campo: `$.entries.tcoeRepulsionShi.activities.n3sMOUPW5gw6plT0.condition`.
- Inglés detectado: After being hit by a melee attack
- Corrección recomendada: Propuesta: "Después de recibir el impacto de un ataque cuerpo a cuerpo".

### ING-08. Lista ampliada de conjuros de hechicero

Estado: **Corregido**.

- Prioridad: **Alta**.
- Archivo: `compendium/dnd-tashas-cauldron.tcoe-character-options.json` (línea 3041).
- Campo: `$.entries.tcoesorSpells000.description`.
- Inglés detectado: Booming Blade, Green-flame Blade, Lightning Lure, Mind Sliver, Sword Burst; Grease; Tasha's Caustic Brew; Flame Blade; Flaming Sphere; Magic Weapon; Tasha's Mind Whip; Intellect Fortress; Vampiric Touch; Fire Shield; Bigby's Hand; Flesh to Stone; Otiluke's Freezing Sphere; Tasha's Otherworldly Guise; Dream of the Blue Veil; Demiplane; Blade of Disaster.
- Corrección recomendada: La tabla conserva 21 nombres ingleses. Traducir todas las filas y armonizar la referencia al Player’s Handbook.

### ING-09. Lanzamiento de conjuros del acompañante

Estado: **Corregido**.

- Prioridad: **Alta**.
- Archivo: `compendium/dnd-tashas-cauldron.tcoe-character-options.json` (línea 3276).
- Campo: `$.entries.tcoeSpellcastSpe.description`.
- Inglés detectado: Mage, Healer, Prodigy; Wizard; Cleric and Druid; Bard and Warlock; mage hand, ray of frost, thunderwave; cure wounds, guidance, sacred flame; eldritch blast, healing word, light.
- Corrección recomendada: Traducir etiquetas de roles, clases, nueve conjuros y la conjunción "and". Mantener los UUID y las claves de &Reference.

### ING-10. Página del historial de cambios

Estado: **Corregido**.

- Prioridad: **Media**.
- Archivo: `compendium/dnd-tashas-cauldron.tcoe-content.json` (línea 469).
- Campo: `$.entries.tcoeChangelog000.pages.3PJULQ1Qbg056sO0.text`.
- Inglés detectado: As part of updating Tasha's for 4.0+ versions…; Feature Enhancements; Bug Fixes.
- Corrección recomendada: El campo completo coincide con la exportación inglesa. Traducir la página, incluidas las etiquetas de enlaces, conservando URLs e identificadores.

### ING-11. Introducción a los objetos mágicos

Estado: **Corregido**.

- Prioridad: **Alta**.
- Archivo: `compendium/dnd-tashas-cauldron.tcoe-content.json` (línea 765).
- Campo: `$.entries.tcoeMagicItems00.pages.yYCrYxuC86LQSwoO.text`.
- Inglés detectado: Mighty Servant of Leuk-o; Who doesn’t love magic items? The desire for them is one of the few things Mordenkainen and I have in common.
- Corrección recomendada: Traducir la etiqueta del artefacto y todo el bloque de comentario de Tasha al final de la página. Revisar también Feywild y Shadowfell según el glosario.

### ING-12. Carpeta sin traducir

Estado: **Corregido**.

- Prioridad: **Media**.
- Archivo: `compendium/dnd-tashas-cauldron.tcoe-magic-items.json` (línea 15).
- Campo: `$.folders.Absorbing Tattoo Colors`.
- Inglés detectado: Absorbing Tattoo Colors
- Corrección recomendada: Propuesta: "Colores de tatuaje absorbente". Cambiar únicamente el valor; conservar la clave inglesa de folders.

### ING-13. Carpeta sin traducir

Estado: **Corregido**.

- Prioridad: **Media**.
- Archivo: `compendium/dnd-tashas-cauldron.tcoe-magic-items.json` (línea 16).
- Campo: `$.folders.Ammunition`.
- Inglés detectado: Ammunition
- Corrección recomendada: Propuesta: "Munición". Cambiar únicamente el valor; conservar la clave inglesa de folders.

### ING-14. Carpeta sin traducir

Estado: **Corregido**.

- Prioridad: **Media**.
- Archivo: `compendium/dnd-tashas-cauldron.tcoe-magic-items.json` (línea 17).
- Campo: `$.folders.Barrier Tattoo Weights`.
- Inglés detectado: Barrier Tattoo Weights
- Corrección recomendada: Propuesta: "Categorías de tatuaje de barrera". Cambiar únicamente el valor; conservar la clave inglesa de folders.

### ING-15. Carpeta sin traducir

Estado: **Corregido**.

- Prioridad: **Media**.
- Archivo: `compendium/dnd-tashas-cauldron.tcoe-magic-items.json` (línea 18).
- Campo: `$.folders.Elemental Shards`.
- Inglés detectado: Elemental Shards
- Corrección recomendada: Propuesta: "Esquirlas elementales". Cambiar únicamente el valor; conservar la clave inglesa de folders.

### ING-16. Carpeta sin traducir

Estado: **Corregido**.

- Prioridad: **Media**.
- Archivo: `compendium/dnd-tashas-cauldron.tcoe-magic-items.json` (línea 19).
- Campo: `$.folders.Firearms`.
- Inglés detectado: Firearms
- Corrección recomendada: Propuesta: "Armas de fuego". Cambiar únicamente el valor; conservar la clave inglesa de folders.

### ING-17. Carpeta sin traducir

Estado: **Corregido**.

- Prioridad: **Media**.
- Archivo: `compendium/dnd-tashas-cauldron.tcoe-magic-items.json` (línea 21).
- Campo: `$.folders.Magic Tattoos`.
- Inglés detectado: Magic Tattoos
- Corrección recomendada: Propuesta: "Tatuajes mágicos". Cambiar únicamente el valor; conservar la clave inglesa de folders.

### ING-18. Carpeta sin traducir

Estado: **Corregido**.

- Prioridad: **Media**.
- Archivo: `compendium/dnd-tashas-cauldron.tcoe-magic-items.json` (línea 22).
- Campo: `$.folders.Outer Shards`.
- Inglés detectado: Outer Shards
- Corrección recomendada: Propuesta: "Esquirlas exteriores". Cambiar únicamente el valor; conservar la clave inglesa de folders.

### ING-19. Carpeta sin traducir

Estado: **Corregido**.

- Prioridad: **Media**.
- Archivo: `compendium/dnd-tashas-cauldron.tcoe-magic-items.json` (línea 23).
- Campo: `$.folders.Supplemental Items`.
- Inglés detectado: Supplemental Items
- Corrección recomendada: Propuesta: "Objetos complementarios". Cambiar únicamente el valor; conservar la clave inglesa de folders.

## Referencias editoriales y términos que requieren criterio

Estos casos se separan de los 19 campos anteriores: son títulos, topónimos, marcas o decisiones terminológicas, no párrafos de reglas enteramente pendientes.

| Archivo / campo | Término | Recomendación |
|---|---|---|
| `compendium/dnd-tashas-cauldron.tcoe-character-options.json` (línea 3041)<br>`$.entries.tcoesorSpells000.description` | Player’s Handbook | Usar "Manual del Jugador" en prosa y mantener coherencia con PHB. |
| `compendium/dnd-tashas-cauldron.tcoe-content.json` (línea 733)<br>`$.entries.tcoeGuild0000000.pages.lwtp3NPFk8lS2Yab.text` | Player's Handbook | Armonizar el título citado. |
| `compendium/dnd-tashas-cauldron.tcoe-magic-items.json` (línea 284)<br>`$.entries.tcoeFeywildShard.description` | Player's Handbook; Feywild | Armonizar título y topónimo. |
| `compendium/dnd-tashas-cauldron.tcoe-magic-items.json` (línea 283)<br>`$.entries.tcoeFeywildShard.name` | Feywild | Valorar "Tierras Salvajes de las Hadas" según el glosario del proyecto. |
| `compendium/dnd-tashas-cauldron.tcoe-magic-items.json` (línea 511)<br>`$.entries.tcoeShadowfellBr.name` | Shadowfell | Valorar "Páramo Sombrío" según el glosario del proyecto. |
| `compendium/dnd-tashas-cauldron.tcoe-magic-items.json` (línea 515)<br>`$.entries.tcoeShadowfellSh.name` | Shadowfell | Aplicar la misma decisión a nombre, descripción y referencias cruzadas. |
| `compendium/dnd-tashas-cauldron.tcoe-tables.json` (línea 2014)<br>`$.entries.tcoeTrinkets0000.results.NSbRFK8zx2qhNIOI.text` | The Wizard of Wines Winery, Red Dragon Crush, 331422-W | Etiqueta ficticia de vino: decidir si se conserva el nombre propio o se localiza; conservar el código. |


También aparecen "Dungeon Master", "Forgotten Realms" y títulos originales de otros libros en créditos y referencias. Revisar el criterio editorial de forma global, sin traducir automáticamente marcas ni nombres de autores.

## Inglés deliberado: no tratar como error

- **Rompecabezas:** `tcoeCreaturePain.pages.rfDlSZp1NbMD3ZVL.text` conserva Werewolf, Beholder, Gelatinous Cubes, Dragons y OWLBEAR para la extracción de letras. La explicación española justifica su presencia.
- **Acertijos:** `tcoeEyeOfTheBeho.pages.FuDcnZ4fQW8qMi0x.text` conserva Eagle, Needle, Window, Newt, Evil eye, Storm y Snake eyes para formar las direcciones del recorrido.
- **Mapa:** `tcoeIllusiveIsla.pages.uWmjVkqII65gHcSh.text` conserva los topónimos de las etiquetas originales entre paréntesis junto con su traducción española.
- **Nombres compartidos o propios:** Galeb Duhr, Dao, Marid, Rakshasa, Flumph, Banshee, nombres de personas, marcas y similares no se clasifican como errores solo por coincidir con la fuente. Celestial, Elemental, Protector, Visual, Aura y Chef tampoco demuestran por sí solos falta de traducción.
- **Sintaxis:** no traducir UUID, rutas de imágenes, claves de `mapping`, claves inglesas de `folders`, `@scale`, `@prof`, `{creature}`, opciones de `@Embed` ni identificadores de `&Reference`. Sí se deben traducir las etiquetas visibles explícitas de los enlaces.

## JSON auxiliares y riesgo de regeneración

Las fuentes inglesas y los campos `source`, `english`, URLs, hashes y estados técnicos son normales en herramientas de desarrollo. Los campos `target` deben revisarse cuando contienen la traducción que se vuelve a publicar. Se han localizado estas réplicas concretas:

| Archivo | Campos que conservan restos |
|---|---|
| `dev-tools/translation/generated/translation-memory.actors.json` | `$[983].target`, `$[1140].target`, `$[1367].target`, `$[1381].target`: conjuros del caballero de la muerte y notas de Foundry. |
| `dev-tools/translation/generated/translation-memory.character-options.json` | `$[608].target`, `$[938].target`, `$[1130].target`, `$[1222].target`: telepatía, compañero primigenio, conjuros de hechicero y lanzamiento de conjuros del acompañante. |
| `dev-tools/translation/reviewed-content.batch-30.json` | `$.entries.tcoeMagicItems00.pages.yYCrYxuC86LQSwoO.text`: conserva el comentario inglés de Tasha y la etiqueta del artefacto. |


Los índices de las listas son de base cero. Al corregir los compendios, actualizar también los insumos correspondientes para que una regeneración no restaure el inglés.

### Clasificación de los demás archivos

- `dev-tools/export/data/*.en.json`: siete fuentes inglesas de referencia; conservar el idioma original.
- `dev-tools/export/_data/*.json`: siete exportaciones auxiliares; no las carga Babele desde `compendium`. No confundirlas con el resultado distribuido.
- `dev-tools/export/_data/extracted/*.es.json`: dos corpus extraídos del PDF, material de referencia que puede conservar nombres propios y artefactos de extracción. No se propone una limpieza automática del corpus.
- Glosarios, memorias, colas de revisión, informes y lotes `reviewed-*`: contienen datos bilingües o técnicos. El inventario contabiliza todos sus valores; el inglés de las fuentes no se suma a los 19 campos de compendios.
- `lang/en.json`: sus dos mensajes ingleses son intencionados.
- `lang/es.json`: sus dos mensajes están en español; el título original del producto se conserva en la descripción.
- `module.json`: `$.title` y `$.description` están en inglés. Son metadatos visibles en el gestor de módulos; valorar traducirlos si se desea una presentación completamente española. `$.languages[0].name` ("English") es una etiqueta de idioma intencionada. Identificadores y enlaces se conservan.

## Interpretación de la auditoría anterior

`dev-tools/translation/generated/report.audit-all.json` indica integridad estructural y cobertura frente a la exportación: no demuestra que todo el contenido está traducido. Un campo puede existir, conservar sus macros y seguir conteniendo texto inglés. Por eso los informes `pending.*` vacíos y el estado `passed` son compatibles con los hallazgos de esta revisión.

## Orden de corrección sugerido

1. Textos de reglas y etiquetas visibles: conjuros, condición de actividad, compañero primigenio, telepatía y acompañante.
2. Introducción a objetos mágicos y carpetas del compendio.
3. Notas de Foundry e historial de cambios.
4. Armonización editorial y actualización de memorias/lotes afectados.
5. Validar JSON y macros y comprobar los documentos en Foundry, incluidas las secciones secretas visibles para el DJ.

## Inventario completo

Número de valores de texto, incluidas cadenas técnicas; no equivale al número de frases visibles o traducibles. Todas las rutas son relativas al módulo.

| Archivo JSON | Valores de texto | Lectura |
|---|---:|---|
| `compendium/dnd-tashas-cauldron.tcoe-actors.json` | 1958 | Válido |
| `compendium/dnd-tashas-cauldron.tcoe-character-options.json` | 1681 | Válido |
| `compendium/dnd-tashas-cauldron.tcoe-content.json` | 468 | Válido |
| `compendium/dnd-tashas-cauldron.tcoe-dm-tools.json` | 293 | Válido |
| `compendium/dnd-tashas-cauldron.tcoe-magic-items.json` | 288 | Válido |
| `compendium/dnd-tashas-cauldron.tcoe-scenes.json` | 5 | Válido |
| `compendium/dnd-tashas-cauldron.tcoe-tables.json` | 807 | Válido |
| `dev-tools/export/_data/dnd-tashas-cauldron.tcoe-actors.json` | 1963 | Válido |
| `dev-tools/export/_data/dnd-tashas-cauldron.tcoe-character-options.json` | 1617 | Válido |
| `dev-tools/export/_data/dnd-tashas-cauldron.tcoe-content.json` | 610 | Válido |
| `dev-tools/export/_data/dnd-tashas-cauldron.tcoe-dm-tools.json` | 339 | Válido |
| `dev-tools/export/_data/dnd-tashas-cauldron.tcoe-magic-items.json` | 439 | Válido |
| `dev-tools/export/_data/dnd-tashas-cauldron.tcoe-scenes.json` | 4 | Válido |
| `dev-tools/export/_data/dnd-tashas-cauldron.tcoe-tables.json` | 773 | Válido |
| `dev-tools/export/_data/extracted/magic-item-pdf-sections.es.json` | 1750 | Válido |
| `dev-tools/export/_data/extracted/tashas-pdf-corpus.es.json` | 14946 | Válido |
| `dev-tools/export/data/dnd-tashas-cauldron.tcoe-actors.en.json` | 4451 | Válido |
| `dev-tools/export/data/dnd-tashas-cauldron.tcoe-character-options.en.json` | 3606 | Válido |
| `dev-tools/export/data/dnd-tashas-cauldron.tcoe-content.en.json` | 1093 | Válido |
| `dev-tools/export/data/dnd-tashas-cauldron.tcoe-dm-tools.en.json` | 637 | Válido |
| `dev-tools/export/data/dnd-tashas-cauldron.tcoe-magic-items.en.json` | 1078 | Válido |
| `dev-tools/export/data/dnd-tashas-cauldron.tcoe-scenes.en.json` | 6 | Válido |
| `dev-tools/export/data/dnd-tashas-cauldron.tcoe-tables.en.json` | 904 | Válido |
| `dev-tools/translation/generated/alignment-warnings.content.json` | 0 | Válido |
| `dev-tools/translation/generated/alignment-warnings.dm-tools.json` | 0 | Válido |
| `dev-tools/translation/generated/alignment-warnings.tables.json` | 135 | Válido |
| `dev-tools/translation/generated/conflicts.actors.json` | 0 | Válido |
| `dev-tools/translation/generated/conflicts.character-options.json` | 0 | Válido |
| `dev-tools/translation/generated/conflicts.content.json` | 0 | Válido |
| `dev-tools/translation/generated/conflicts.dm-tools.json` | 0 | Válido |
| `dev-tools/translation/generated/glossary.actors.json` | 1022 | Válido |
| `dev-tools/translation/generated/glossary.character-options.json` | 1218 | Válido |
| `dev-tools/translation/generated/pending.content.json` | 0 | Válido |
| `dev-tools/translation/generated/pending.dm-tools.json` | 0 | Válido |
| `dev-tools/translation/generated/pending.magic-items.json` | 0 | Válido |
| `dev-tools/translation/generated/pending.tables.json` | 0 | Válido |
| `dev-tools/translation/generated/protected-token-issues.actors.json` | 0 | Válido |
| `dev-tools/translation/generated/protected-token-issues.character-options.json` | 0 | Válido |
| `dev-tools/translation/generated/protected-token-issues.content.json` | 0 | Válido |
| `dev-tools/translation/generated/protected-token-issues.dm-tools.json` | 0 | Válido |
| `dev-tools/translation/generated/protected-token-issues.tables.json` | 0 | Válido |
| `dev-tools/translation/generated/report.actors.json` | 1 | Válido |
| `dev-tools/translation/generated/report.audit-all.json` | 14 | Válido |
| `dev-tools/translation/generated/report.character-options.json` | 1 | Válido |
| `dev-tools/translation/generated/report.content.json` | 1 | Válido |
| `dev-tools/translation/generated/report.dm-tools.json` | 1 | Válido |
| `dev-tools/translation/generated/report.magic-item-pdf-extraction.json` | 10 | Válido |
| `dev-tools/translation/generated/report.magic-item-review-queue.json` | 31 | Válido |
| `dev-tools/translation/generated/report.magic-items.json` | 2 | Válido |
| `dev-tools/translation/generated/report.pdf-corpus.json` | 0 | Válido |
| `dev-tools/translation/generated/report.process-summary.json` | 8 | Válido |
| `dev-tools/translation/generated/report.scenes.json` | 1 | Válido |
| `dev-tools/translation/generated/report.tables.json` | 1 | Válido |
| `dev-tools/translation/generated/review-queue.magic-items.json` | 2539 | Válido |
| `dev-tools/translation/generated/translation-memory.actors.json` | 8525 | Válido |
| `dev-tools/translation/generated/translation-memory.character-options.json` | 7955 | Válido |
| `dev-tools/translation/generated/translation-memory.magic-items.json` | 1638 | Válido |
| `dev-tools/translation/official-content-terms.json` | 16 | Válido |
| `dev-tools/translation/official-dm-tools-terms.json` | 0 | Válido |
| `dev-tools/translation/official-magic-item-names.json` | 138 | Válido |
| `dev-tools/translation/protected-token-overrides.tables.json` | 2 | Válido |
| `dev-tools/translation/reviewed-content.batch-04.json` | 20 | Válido |
| `dev-tools/translation/reviewed-content.batch-05.json` | 20 | Válido |
| `dev-tools/translation/reviewed-content.batch-06.json` | 10 | Válido |
| `dev-tools/translation/reviewed-content.batch-07.json` | 10 | Válido |
| `dev-tools/translation/reviewed-content.batch-08.json` | 6 | Válido |
| `dev-tools/translation/reviewed-content.batch-09.json` | 12 | Válido |
| `dev-tools/translation/reviewed-content.batch-10.json` | 12 | Válido |
| `dev-tools/translation/reviewed-content.batch-11.json` | 10 | Válido |
| `dev-tools/translation/reviewed-content.batch-12.json` | 8 | Válido |
| `dev-tools/translation/reviewed-content.batch-13.json` | 8 | Válido |
| `dev-tools/translation/reviewed-content.batch-14.json` | 8 | Válido |
| `dev-tools/translation/reviewed-content.batch-15.json` | 8 | Válido |
| `dev-tools/translation/reviewed-content.batch-16.json` | 8 | Válido |
| `dev-tools/translation/reviewed-content.batch-17.json` | 8 | Válido |
| `dev-tools/translation/reviewed-content.batch-18.json` | 8 | Válido |
| `dev-tools/translation/reviewed-content.batch-19.json` | 8 | Válido |
| `dev-tools/translation/reviewed-content.batch-20.json` | 8 | Válido |
| `dev-tools/translation/reviewed-content.batch-21.json` | 8 | Válido |
| `dev-tools/translation/reviewed-content.batch-22.json` | 4 | Válido |
| `dev-tools/translation/reviewed-content.batch-23.json` | 2 | Válido |
| `dev-tools/translation/reviewed-content.batch-24.json` | 126 | Válido |
| `dev-tools/translation/reviewed-content.batch-25.json` | 1 | Válido |
| `dev-tools/translation/reviewed-content.batch-26.json` | 1 | Válido |
| `dev-tools/translation/reviewed-content.batch-27.json` | 1 | Válido |
| `dev-tools/translation/reviewed-content.batch-28.json` | 1 | Válido |
| `dev-tools/translation/reviewed-content.batch-29.json` | 4 | Válido |
| `dev-tools/translation/reviewed-content.batch-30.json` | 1 | Válido |
| `dev-tools/translation/reviewed-content.batch-31.json` | 1 | Válido |
| `dev-tools/translation/reviewed-content.batch-32.json` | 4 | Válido |
| `dev-tools/translation/reviewed-content.json` | 64 | Válido |
| `dev-tools/translation/reviewed-dm-tools.batch-02.json` | 20 | Válido |
| `dev-tools/translation/reviewed-dm-tools.batch-03.json` | 20 | Válido |
| `dev-tools/translation/reviewed-dm-tools.batch-04.json` | 8 | Válido |
| `dev-tools/translation/reviewed-dm-tools.batch-05.json` | 8 | Válido |
| `dev-tools/translation/reviewed-dm-tools.batch-06.json` | 8 | Válido |
| `dev-tools/translation/reviewed-dm-tools.batch-07.json` | 4 | Válido |
| `dev-tools/translation/reviewed-dm-tools.batch-08.json` | 10 | Válido |
| `dev-tools/translation/reviewed-dm-tools.batch-09.json` | 8 | Válido |
| `dev-tools/translation/reviewed-dm-tools.batch-10.json` | 10 | Válido |
| `dev-tools/translation/reviewed-dm-tools.batch-11.json` | 8 | Válido |
| `dev-tools/translation/reviewed-dm-tools.batch-12.json` | 6 | Válido |
| `dev-tools/translation/reviewed-dm-tools.batch-13.json` | 8 | Válido |
| `dev-tools/translation/reviewed-dm-tools.batch-14.json` | 8 | Válido |
| `dev-tools/translation/reviewed-dm-tools.batch-15.json` | 8 | Válido |
| `dev-tools/translation/reviewed-dm-tools.batch-16.json` | 8 | Válido |
| `dev-tools/translation/reviewed-dm-tools.batch-17.json` | 8 | Válido |
| `dev-tools/translation/reviewed-dm-tools.batch-18.json` | 4 | Válido |
| `dev-tools/translation/reviewed-dm-tools.batch-19.json` | 6 | Válido |
| `dev-tools/translation/reviewed-dm-tools.batch-20.json` | 4 | Válido |
| `dev-tools/translation/reviewed-dm-tools.batch-21.json` | 4 | Válido |
| `dev-tools/translation/reviewed-dm-tools.batch-22.json` | 90 | Válido |
| `dev-tools/translation/reviewed-dm-tools.batch-23.json` | 2 | Válido |
| `dev-tools/translation/reviewed-dm-tools.batch-24.json` | 3 | Válido |
| `dev-tools/translation/reviewed-dm-tools.batch-25.json` | 3 | Válido |
| `dev-tools/translation/reviewed-dm-tools.batch-26.json` | 2 | Válido |
| `dev-tools/translation/reviewed-dm-tools.batch-27.json` | 3 | Válido |
| `dev-tools/translation/reviewed-dm-tools.json` | 20 | Válido |
| `dev-tools/translation/reviewed-magic-item-descriptions.json` | 130 | Válido |
| `dev-tools/translation/reviewed-tables.json` | 803 | Válido |
| `dev-tools/translation/upstream-issues.magic-items.json` | 5 | Válido |
| `dev-tools/translation/upstream-issues.tables.json` | 10 | Válido |
| `lang/en.json` | 2 | Válido |
| `lang/es.json` | 2 | Válido |
| `module.json` | 37 | Válido |
