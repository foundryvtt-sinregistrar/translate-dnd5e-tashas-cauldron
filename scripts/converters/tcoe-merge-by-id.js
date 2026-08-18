export function mergeById(source, translation) {
  if (!source || typeof source !== "object" || !translation || typeof translation !== "object") {
    return source;
  }

  const out = foundry.utils.deepClone(source);
  for (const [id, patch] of Object.entries(translation)) {
    if (!patch || typeof patch !== "object") continue;

    if (Array.isArray(out)) {
      const target = out.find((row) => (row?._id ?? row?.id) === id);
      if (target) foundry.utils.mergeObject(target, patch, { insertKeys: true, overwrite: true, inplace: true });
      continue;
    }

    if (out[id]) {
      foundry.utils.mergeObject(out[id], patch, { insertKeys: true, overwrite: true, inplace: true });
    }
  }
  return out;
}

export const tcoeActivitiesById = mergeById;
export const tcoeEffectsById = mergeById;
export const tcoeAdvancementById = mergeById;
export const tcoeTableResultsById = mergeById;

export function tcoeActorItemsById(source, translation) {
  if (!Array.isArray(source) || !translation || typeof translation !== "object") return source;

  const out = foundry.utils.deepClone(source);
  for (const item of out) {
    const id = item?._id ?? item?.id;
    const patch = id ? translation[id] : null;
    if (!patch || typeof patch !== "object") continue;

    if (typeof patch.name === "string") item.name = patch.name;
    if (typeof patch.description === "string") {
      item.system ??= {};
      item.system.description ??= {};
      item.system.description.value = patch.description;
    }
    if (patch.activities) {
      item.system ??= {};
      item.system.activities = mergeById(item.system.activities ?? {}, patch.activities);
    }
    if (patch.effects) item.effects = mergeById(item.effects ?? [], patch.effects);
    if (patch.advancement) {
      item.system ??= {};
      item.system.advancement = mergeById(item.system.advancement ?? [], patch.advancement);
    }
  }
  return out;
}
