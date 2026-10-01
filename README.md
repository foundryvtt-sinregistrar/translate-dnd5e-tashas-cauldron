# El caldero de Tasha para todo — Traducción al español

**Versión actual — Foundry v14**

![Foundry v14](https://img.shields.io/badge/Foundry-v14-green)
[![Release v1.14.3](https://img.shields.io/badge/release-v1.14.3-blue)](https://github.com/foundryvtt-sinregistrar/translate-dnd5e-tashas-cauldron/releases/tag/v1.14.3)
![dnd5e 6.0.3](https://img.shields.io/badge/dnd5e-6.0.3-blue)
![Babele 2.9.1 required](https://img.shields.io/badge/Babele-2.9.1_required-orange)
![Tasha required](https://img.shields.io/badge/Tasha-required-orange)

**Español** | [English](README.en.md)

Traducción para Foundry VTT mediante Babele. Identificador: `translate-dnd5e-tashas-cauldron`.

## Estado

Versión: **1.14.3**. Incluye traducciones de siete compendios mediante Babele y convertidores con prefijo `tcoe`. Las pruebas de registro y cobertura no acreditan una validación funcional completa. Se conserva el nombre histórico del ZIP terminado en `-es.zip`.

Consulta [CHANGELOG.md](CHANGELOG.md).

Comprobación del 28 de septiembre de 2026 en Foundry 14.368, dnd5e 6.0.3 y Babele 2.9.1: lectura de 837 documentos en 7 compendios, comprobación de nombres y campos de texto explícitos e importación y revisión visual de una muestra. No es una revisión lingüística ni funcional exhaustiva; permanecen algunas etiquetas inglesas del contenido original.

## Requisitos

Versiones declaradas en el manifiesto; «—» indica que no se declara ese límite.

| Dependencia | Mínima | Verificada |
|---|---|---|
| Foundry VTT | 14.367 | 14.368 |
| dnd5e | 6.0.0 | 6.0.3 |
| babele | 2.9.1 | 2.9.1 |
| dnd-tashas-cauldron | 4.0.0 | 4.0.0 |

Instala y activa las dependencias, adquiriendo por separado los productos oficiales cuando sean necesarios.

## Instalación

En la configuración de Foundry, abre **Add-on Modules → Install Module** y utiliza este manifiesto:

```text
https://github.com/foundryvtt-sinregistrar/translate-dnd5e-tashas-cauldron/releases/latest/download/module.json
```

Para instalar manualmente, descarga `translate-dnd5e-tashas-cauldron-es.zip` de las [releases](https://github.com/foundryvtt-sinregistrar/translate-dnd5e-tashas-cauldron/releases). Con Foundry detenido, extrae la carpeta `translate-dnd5e-tashas-cauldron` en `Data/modules/`; el manifiesto debe quedar en `Data/modules/translate-dnd5e-tashas-cauldron/module.json`.

## Activación

1. Abre un mundo dnd5e.
2. Activa Babele, sus dependencias, los productos oficiales requeridos y esta traducción.
3. Selecciona **Español** y recarga el mundo.
4. Abre un compendio traducido para comprobar el resultado.

El registro es automático para `es` y sus variantes regionales. Otros idiomas no activan la traducción española.

## Actualización

Actualiza desde Foundry o sustituye la carpeta con el ZIP publicado y Foundry detenido. Recarga el mundo. Las copias ya importadas no se sincronizan automáticamente: revisa las diferencias antes de sustituir documentos con cambios propios.

## Contenido incluido

- `dnd-tashas-cauldron.tcoe-actors.json`.
- `dnd-tashas-cauldron.tcoe-character-options.json`.
- `dnd-tashas-cauldron.tcoe-content.json`.
- `dnd-tashas-cauldron.tcoe-dm-tools.json`.
- `dnd-tashas-cauldron.tcoe-magic-items.json`.
- `dnd-tashas-cauldron.tcoe-scenes.json`.
- `dnd-tashas-cauldron.tcoe-tables.json`.

## Limitaciones

La cobertura textual y las pruebas automáticas no acreditan todas las automatizaciones de una partida. Conserva las limitaciones indicadas en Estado. Las copias importadas no se actualizan automáticamente. Las nuevas URLs de release necesitan una publicación con sus adjuntos; mientras no estén disponibles, utiliza un ZIP validado. No se distribuyen fuentes privadas, PDF, OCR ni exportaciones oficiales completas.

## Soporte y contribuciones

Comunica errores en las [incidencias](https://github.com/foundryvtt-sinregistrar/translate-dnd5e-tashas-cauldron/issues), indicando versiones, compendio/documento afectado, pasos, resultado esperado y observado, y si se trata de una copia importada.

## Desarrollo

La [guía de desarrollo](https://github.com/foundryvtt-sinregistrar/translate-dnd5e-tashas-cauldron/blob/main/DEVELOPER.md) está disponible en el repositorio y se excluye del ZIP instalable.

## Licencia y créditos

Consulta la licencia y sus condiciones en [LICENSE.md](LICENSE.md). Se conserva la licencia Apache 2.0 existente.

Traducción no oficial, sin afiliación con Wizards of the Coast ni Foundry VTT. Los materiales del producto oficial pertenecen a sus respectivos titulares. Autor del módulo: [foundryvtt-sinregistrar](https://github.com/foundryvtt-sinregistrar).
