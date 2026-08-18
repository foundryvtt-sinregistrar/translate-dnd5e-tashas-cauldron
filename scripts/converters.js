/** Punto de entrada reservado para los convertidores estructurados de Babele. */
Hooks.on("init", () => {
  const babele = game?.babele;
  if (!babele?.registerConverters) return;
  babele.registerConverters({});
});
