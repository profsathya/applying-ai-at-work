import guidance from './walkthrough-guidance.json' with {type: 'json'};

/** Shared with the artifact validator; criteria never come from browser requests. */
export const WALKTHROUGH_GUIDANCE: Record<string, {
  title: string;
  rule: string;
  checkpoints: Record<string, string>;
}> = guidance;
