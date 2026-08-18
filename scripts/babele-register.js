/** Registra los compendios oficiales de Tasha en Babele. */
Hooks.on("init", () => {
  const babele = game?.babele;
  if (!babele) return;

  const current = game.i18n?.lang ?? "es";
  const langs = Array.from(new Set([current, current.split("-")[0]]));
  const compendium = {
    "dnd-tashas-cauldron.tcoe-content": { label: "Tasha - Contenido", path: "dnd-tashas-cauldron.tcoe-content.json" },
    "dnd-tashas-cauldron.tcoe-character-options": { label: "Tasha - Opciones de personaje", path: "dnd-tashas-cauldron.tcoe-character-options.json" },
    "dnd-tashas-cauldron.tcoe-magic-items": { label: "Tasha - Objetos mágicos", path: "dnd-tashas-cauldron.tcoe-magic-items.json" },
    "dnd-tashas-cauldron.tcoe-tables": { label: "Tasha - Tablas", path: "dnd-tashas-cauldron.tcoe-tables.json" },
    "dnd-tashas-cauldron.tcoe-actors": { label: "Tasha - Actores", path: "dnd-tashas-cauldron.tcoe-actors.json" },
    "dnd-tashas-cauldron.tcoe-dm-tools": { label: "Tasha - Herramientas del DM", path: "dnd-tashas-cauldron.tcoe-dm-tools.json" },
    "dnd-tashas-cauldron.tcoe-scenes": { label: "Tasha - Escenas", path: "dnd-tashas-cauldron.tcoe-scenes.json" }
  };

  for (const lang of langs) {
    babele.register({ module: "translate-dnd5e-tashas-cauldron", lang, dir: "compendium", compendium });
  }
});
