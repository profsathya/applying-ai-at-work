/** Reviewed course criteria live here, never in browser-supplied requests. */
export const WALKTHROUGH_GUIDANCE: Record<string, {
  title: string;
  rule: string;
  checkpoints: Record<string, string>;
}> = {
  // Add an entry when a reviewed Canvas walk-through is authored. The key must
  // equal its stable artifact_id; checkpoint keys must equal guided task IDs.
};
