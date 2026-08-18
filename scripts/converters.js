import {
  tcoeActivitiesById,
  tcoeEffectsById,
  tcoeAdvancementById,
  tcoeActorItemsById,
  tcoeTableResultsById
} from "./converters/tcoe-merge-by-id.js";

/** Convertidores estructurados de Babele para los documentos de Tasha. */
Hooks.on("init", () => {
  const babele = game?.babele;
  if (!babele?.registerConverters) return;
  babele.registerConverters({
    tcoeActivitiesById,
    tcoeEffectsById,
    tcoeAdvancementById,
    tcoeActorItemsById,
    tcoeTableResultsById
  });
});
