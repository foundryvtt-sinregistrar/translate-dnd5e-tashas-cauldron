# Informe final de traducción de Tasha

## Resultado

La traducción del módulo `dnd-tashas-cauldron` para Foundry VTT 14 se ha procesado por completo en la rama `develop`. Los siete compendios distribuidos por el módulo tienen cobertura de entradas completa y la auditoría integral termina con estado `passed`.

- Módulo de traducción: `translate-dnd5e-tashas-cauldron`
- Versión: `0.1.0`
- Foundry VTT mínimo: `14`
- Foundry VTT verificado: `14.363`
- Compendios auditados: 7
- Entradas de nivel superior: 837 de 837
- Páginas de diario: 399 de 399 en `tcoe-content` y `tcoe-dm-tools`
- Objetos incrustados en actores: 735 de 735
- Resultados de tablas: 663 de 663
- Referencias internas comprobadas: 1386
- Referencias internas rotas: 0
- Campos pendientes: 0
- Conflictos de memoria de traducción: 0
- Problemas de tokens protegidos: 0
- Campos con mojibake: 0

El informe técnico autoritativo y legible por máquinas es `report.audit-all.json`.

## Cobertura por compendio

| Compendio | Entradas | Cobertura adicional | Estado |
| --- | ---: | --- | --- |
| `tcoe-actors` | 152/152 | 735/735 objetos incrustados; 1705 pares de memoria; 511 términos de glosario | Completo |
| `tcoe-character-options` | 407/407 | 1591 pares de memoria; 609 términos de glosario; no requiere una nueva exportación | Completo |
| `tcoe-magic-items` | 143/143 | 143 nombres; 130/130 descripciones de origen no vacías; 13 entradas sin descripción en origen | Completo |
| `tcoe-tables` | 71/71 | 663/663 resultados; 776 campos traducidos | Completo |
| `tcoe-content` | 39/39 | 252/252 páginas; 0 pendientes | Completo |
| `tcoe-dm-tools` | 23/23 | 147/147 páginas; 0 pendientes | Completo |
| `tcoe-scenes` | 2/2 | 1 carpeta traducida; 0 notas de escena en origen | Completo |

## Fuentes y método

El proceso utilizó tres capas de evidencia, por orden de prioridad:

1. Exportaciones actuales de Foundry VTT 14 almacenadas en `dev-tools/export/data`, que proporcionan los ID autoritativos.
2. Exportaciones españolas previas de `_data`, utilizadas como memoria de traducción cuando la estructura seguía alineada.
3. El corpus PDF español extraído, empleado para terminología oficial, nombres y revisión editorial.

Las traducciones revisadas se dividieron en lotes pequeños bajo `dev-tools/translation/reviewed-*.json`. Los constructores vuelven a generar los compendios finales sin modificar los ID originales. Las memorias y glosarios generados permiten reutilizar únicamente correspondencias no ambiguas; las colisiones se notifican y no se aplican automáticamente.

## Integridad de Foundry y Babele

Durante la generación se conservaron y compararon como tokens protegidos:

- `@UUID[...]`
- `@Embed[...]` y `@embed[...]`
- `&Reference[...]` y `&amp;Reference[...]`
- Tiradas y acciones en línea `[[...]]`

La validación es insensible a mayúsculas y minúsculas para las directivas de Foundry. Los diarios usan el conversor `tcoeJournalPagesById`; actividades, efectos, avances y documentos incrustados se combinan por ID mediante los conversores del módulo.

La auditoría final también comprueba:

- JSON válido para fuentes y salidas.
- Igualdad exacta de conjuntos de ID de entrada.
- Igualdad exacta de ID de página para los dos diarios.
- Igualdad exacta de los 735 ID de objetos de actores.
- Igualdad exacta de los 663 ID de resultados de tablas.
- Existencia de los destinos de las 1386 referencias internas a compendios de Tasha.
- Existencia de los cuatro archivos declarados por `module.json` en `languages` y `esmodules`.
- Ausencia de secuencias habituales de texto UTF-8 mal decodificado.

## Adaptaciones funcionales de rompecabezas

No se tradujeron literalmente los acertijos cuando hacerlo rompía su solución. Se aplicaron estas adaptaciones verificadas:

- **Solo para miembros:** se recalcularon contraseña y ejemplos con números españoles. Los intercambios de ejemplo distinguen correctamente respuestas válidas e inválidas.
- **¿Qué hay en el menú?:** se adaptaron platos y precios para que la operación española produzca `QUIMERA`.
- **No es oro todo lo que reluce:** cantidades, iniciales de espíritus y tabla se recalcularon para que el orden alfabético español revele `EN LA PALMA`. Una prueba adicional verifica las nueve cantidades y todas las iniciales.
- **El ojo del contemplador:** se tradujo la narración y se conservaron de forma explícita las respuestas inglesas cuyos acrónimos forman la ruta `E-N-W-N-E-S-S` de la ficha original.
- **Cuadros de criaturas:** se conserva `OWLBEAR` como clave mecánica de la ilustración original y se explica su equivalencia `oso lechuza` en español.
- **Isla ilusoria:** los topónimos se muestran traducidos junto a las etiquetas inglesas exactas del mapa original.
- **Pasos temerarios:** se tradujeron conjuntamente descripción, trampas y variantes; los términos ligados a la sopa de letras y la solución se mantuvieron coherentes.
- **Cuatro elementos** y **Llaves maestras:** se conservaron geometría, cantidades, tiradas, enlaces y asociaciones visuales.

## Campos revisados sin cambios

Dos campos de `tcoe-content` están marcados explícitamente como `reviewedUnchanged`:

1. El índice de descripciones de objetos mágicos, porque contiene únicamente directivas dinámicas `@UUID` y `@Embed`, sin prosa estática traducible.
2. El historial técnico de la versión premium `2.0.0`, porque contiene diagnósticos de migración y textos de incidencias de GitHub cuya redacción original se conserva como referencia técnica autoritativa.

Estos campos se incluyen en la salida y en la cobertura, pero no se presentan falsamente como traducciones editoriales.

## Diagnósticos no bloqueantes

El constructor de tablas conserva 45 avisos históricos de alineación respecto a la exportación española antigua. No representan resultados ausentes: la auditoría actual confirma los 663 resultados de la exportación inglesa vigente y cero ID faltantes o adicionales. Se mantienen como trazabilidad de que la fuente heredada utilizaba identificadores distintos en esas filas.

## Automatización reproducible

Constructores principales:

```text
python dev-tools/translation/build_actors.py
python dev-tools/translation/build_character_options.py
python dev-tools/translation/build_magic_items.py
python dev-tools/translation/build_tables.py
python dev-tools/translation/build_content.py
python dev-tools/translation/build_dm_tools.py
python dev-tools/translation/build_scenes.py
```

Auditoría final:

```text
python dev-tools/translation/audit_all_compendiums.py
```

Los generadores `generate_magic_items_overview.py` y `generate_book_overview.py` sincronizan los nombres visibles de índices con los compendios ya validados, evitando duplicar terminología manualmente.

## Trazabilidad Git

El historial de `develop` contiene 126 commits desde la inicialización del módulo hasta la primera auditoría global. El trabajo se segmentó por infraestructura, compendio, familias temáticas y adaptaciones de puzles. Todos los mensajes de commit están en inglés.

Los commits de cierre más relevantes son:

- `09d4ea8` — clasificación del historial técnico de origen.
- `559aa3a` — cobertura nominal completa de herramientas del DM.
- `5a16716` — orientación de sesión cero.
- `e138cb6` — adaptación de Pasos temerarios.
- `cf47de8` — adaptación de puzles ilustrados.
- `66d9ba2` — adaptación del Ojo del contemplador.
- `80621b4` — adaptación española de No es oro todo lo que reluce.
- `bb89b79` — auditoría global reproducible.

## Resultado de entrega

Los compendios listos para Babele se encuentran en `compendium/`. El árbol generado puede reproducirse desde los exportes de desarrollo, y el criterio de finalización queda demostrado por los informes individuales y por `report.audit-all.json` con estado `passed`.
