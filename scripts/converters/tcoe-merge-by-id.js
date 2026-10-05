import { translateById, activityPaths, effectPaths, tablePaths, scenePaths } from "./text-only.js";

// Retained export for callers localizing general labels.
export const mergeById = (source, translation) => translateById(source, translation, scenePaths);
export const tcoeActivitiesById = (source, translation) => translateById(source, translation, activityPaths, "activity");
export const tcoeEffectsById = (source, translation) => translateById(source, translation, effectPaths);
export const tcoeAdvancementById = (source, translation) => translateById(source, translation, ["hint"], "advancement");
export const tcoeTableResultsById = (source, translation) => translateById(source, translation, tablePaths);

export function tcoeJournalPagesById(source, translation) {
  if (!source || !translation || typeof translation !== "object") return source;
  const out = foundry.utils.deepClone(source);
  const pages = Array.isArray(out) ? out : Array.from(out?.contents ?? Object.values(out));
  for (const page of pages) {
    const id = page?._id ?? page?.id;
    const patch = id ? translation[id] : null;
    if (!patch || typeof patch !== "object") continue;
    if (typeof patch.name === "string") page.name = patch.name;
    if (typeof patch.text === "string") {
      if (typeof page.text === "string") page.text = patch.text;
      else {
        page.text ??= {};
        page.text.content = patch.text;
        page.text.format ??= 1;
      }
    }
  }
  return out;
}

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
    item.system.activities = tcoeActivitiesById(item.system.activities ?? {}, patch.activities);
    }
    if (patch.effects) item.effects = tcoeEffectsById(item.effects ?? [], patch.effects);
    if (patch.advancement) {
      item.system ??= {};
    item.system.advancement = tcoeAdvancementById(item.system.advancement ?? [], patch.advancement);
    }
  }
  return out;
}
