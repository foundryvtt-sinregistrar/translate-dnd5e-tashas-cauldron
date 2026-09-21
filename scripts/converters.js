import {
  tcoeActivitiesById,
  tcoeEffectsById,
  tcoeAdvancementById,
  tcoeActorItemsById,
  tcoeTableResultsById,
  tcoeJournalPagesById
} from "./converters/tcoe-merge-by-id.js";

/** Convertidores estructurados de Babele para los documentos de Tasha. */
Hooks.once("babele.init", (babele) => {
  if (!babele?.registerConverters) return;

  // Core settings exist at setup, before Babele loads translations at ready.
  Hooks.once("setup", () => {
    const language = game.settings.get("core", "language");
    if (typeof language !== "string" || language.split("-")[0].toLowerCase() !== "es") return;

    babele.registerConverters({
      tcoeActivitiesById,
      tcoeEffectsById,
      tcoeAdvancementById,
      tcoeActorItemsById,
      tcoeTableResultsById,
      tcoeJournalPagesById
    });
  });
});
