# Extracción de los compendios de Tasha

1. Inicia Foundry VTT y abre un mundo con el sistema `dnd5e`.
2. Activa `dnd-tashas-cauldron`. Para extraer no es necesario activar Babele ni este módulo de traducción.
3. Pulsa `F12` y abre la pestaña **Console** de las herramientas del navegador.
4. Abre `export-tashas-compendiums.js`, copia el archivo completo, pégalo en la consola y ejecútalo.
5. El navegador descargará siete archivos terminados en `.en.json`. Si bloquea descargas múltiples, autorízalas para la dirección de Foundry y repite la ejecución.
6. Conserva esos ficheros como referencia inglesa en `dev-tools/export/data/`. Copia después cada estructura a su archivo correspondiente de `compendium/` para traducir solo los valores, nunca los IDs ni las claves estructurales.

La constante `PACKS` permite exportar solo un compendio. Durante el trabajo por
fases se configura con el siguiente compendio que debe regenerarse. Restaura
las demás entradas cuando sea necesario regenerarlos todos.

El exportador usa la API de Foundry (`game.packs`) y no accede directamente a los ficheros LevelDB del módulo premium.
