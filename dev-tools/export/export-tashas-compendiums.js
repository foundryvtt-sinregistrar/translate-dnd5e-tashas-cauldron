/**
 * Exporta los siete compendios de Tasha a JSON de referencia para Babele.
 * Uso: ejecutar el contenido completo en la consola del navegador (F12)
 * dentro de un mundo con dnd-tashas-cauldron activo.
 */
(async () => {
  const MODULE_ID = "dnd-tashas-cauldron";
  const PACKS = [
    "tcoe-content",
    "tcoe-character-options",
    "tcoe-magic-items",
    "tcoe-tables",
    "tcoe-actors",
    "tcoe-dm-tools",
    "tcoe-scenes"
  ];

  const text = (value) => typeof value === "string" ? value : "";
  const object = (value) => value && typeof value === "object" && !Array.isArray(value) ? value : {};
  const get = (source, path, fallback = undefined) => {
    const value = foundry.utils.getProperty(source, path);
    return value === undefined ? fallback : value;
  };
  const sortObject = (value) => Object.fromEntries(
    Object.entries(object(value)).sort(([a], [b]) => a.localeCompare(b, undefined, { numeric: true }))
  );
  const byId = (values, mapper) => {
    const rows = Array.from(values?.contents ?? values ?? []);
    return sortObject(Object.fromEntries(rows.flatMap((row) => {
      const id = row?.id ?? row?._id;
      return id ? [[id, mapper(row)]] : [];
    })));
  };
  const folders = (pack) => {
    const rows = Array.from(pack.folders?.contents ?? pack.folders ?? []);
    return Object.fromEntries(rows.map((folder) => folder?.name).filter(Boolean).sort().map((name) => [name, name]));
  };
  const save = (payload, filename) => {
    const json = JSON.stringify(payload, null, 2);
    if (typeof saveDataToFile === "function") return saveDataToFile(json, "application/json", filename);
    const url = URL.createObjectURL(new Blob([json], { type: "application/json" }));
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = filename;
    anchor.click();
    setTimeout(() => URL.revokeObjectURL(url), 1500);
  };

  const activity = (row) => ({
    name: text(row?.name),
    condition: text(get(row, "activation.condition", "")),
    chatFlavor: text(get(row, "description.chatFlavor", ""))
  });
  const effect = (row) => ({
    name: text(row?.name),
    description: text(row?.description ?? get(row, "description.value", ""))
  });
  const advancement = (row) => ({ title: text(row?.title), hint: text(row?.hint) });
  const item = (document) => {
    const row = document.toObject ? document.toObject() : document;
    return {
      name: text(row?.name),
      description: text(get(row, "system.description.value", "")),
      activities: sortObject(Object.fromEntries(
        Object.entries(object(get(row, "system.activities", {}))).map(([id, value]) => [id, activity(value)])
      )),
      effects: byId(row?.effects, effect),
      advancement: byId(get(row, "system.advancement", []), advancement)
    };
  };
  const journal = (document) => ({
    name: text(document.name),
    folder: text(document.folder?.name),
    pages: byId(document.pages, (page) => {
      const row = page.toObject ? page.toObject() : page;
      return {
        name: text(row?.name),
        type: text(row?.type),
        text: text(get(row, "text.content", row?.text)),
        src: text(row?.src)
      };
    })
  });
  const actor = (document) => {
    const row = document.toObject();
    return {
      name: text(row?.name),
      folder: text(document.folder?.name),
      biography: text(get(row, "system.details.biography.value", "")),
      effects: byId(row?.effects, effect),
      items: byId(row?.items, item)
    };
  };
  const table = (document) => ({
    name: text(document.name),
    folder: text(document.folder?.name),
    description: text(document.description),
    results: byId(document.results, (result) => ({
      text: text(result.text),
      range: Array.isArray(result.range) ? result.range : []
    }))
  });
  const scene = (document) => {
    const row = document.toObject();
    return {
      name: text(row?.name),
      navigation: text(row?.navName),
      notes: byId(row?.notes, (note) => ({ text: text(note?.text) }))
    };
  };

  for (const packName of PACKS) {
    const packId = `${MODULE_ID}.${packName}`;
    const pack = game.packs.get(packId);
    if (!pack) throw new Error(`No se encuentra el compendio ${packId}. Activa el módulo oficial de Tasha.`);

    const documents = await pack.getDocuments();
    const type = pack.documentName ?? pack.metadata?.type;
    const mapper = type === "JournalEntry" ? journal
      : type === "Item" ? item
      : type === "Actor" ? actor
      : type === "RollTable" ? table
      : type === "Scene" ? scene
      : (document) => ({ name: text(document.name) });
    const entries = Object.fromEntries(documents.map((document) => [document.id, mapper(document)]));
    const output = {
      label: pack.metadata?.label ?? pack.title ?? packName,
      folders: folders(pack),
      entries: sortObject(entries)
    };

    save(output, `${packId}.en.json`);
    console.log(`[Tasha export] ${packId}: ${documents.length} documentos (${type})`);
  }

  ui.notifications.info("Exportación de Tasha terminada: se han generado siete descargas JSON.");
})();
