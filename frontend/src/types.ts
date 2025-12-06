export interface DebateTurn {
  speaker: string;
  content: string;
}

export interface DebateResult {
  transcript: DebateTurn[];
  winner: string;
  confidence: number;
  reason: string;
}
