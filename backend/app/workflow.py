from app.agents.definitions import debater_a, debater_b, judge
from app.models import DebateResult, DebateTurn
import json
import re

class DebateWorkflow:
    def __init__(self):
        self.transcript = []

    async def run(self, topic: str) -> DebateResult:
        self.transcript = []
        
        # --- Round 1 ---
        
        # Debater A (Opening)
        prompt_a1 = f"""Topic: {topic}
        
Produce your opening argument.
Start with 'FINAL_ANSWER: YES'."""
        
        response_a1 = debater_a.generate(prompt_a1)
        self.transcript.append(DebateTurn(speaker="Debater A", content=response_a1))
        
        # Debater B (Counter)
        prompt_b1 = f"""Topic: {topic}
        
Debater A's Argument:
{response_a1}

Produce your counter-argument and critique.
Start with 'FINAL_ANSWER: NO'."""
        
        response_b1 = debater_b.generate(prompt_b1)
        self.transcript.append(DebateTurn(speaker="Debater B", content=response_b1))
        
        # --- Round 2 ---
        
        # Debater A (Rebuttal)
        prompt_a2 = f"""Topic: {topic}
        
Debater B's Counter-Argument:
{response_b1}

Produce your rebuttal.
Start with 'FINAL_ANSWER: YES'."""
        
        response_a2 = debater_a.generate(prompt_a2)
        self.transcript.append(DebateTurn(speaker="Debater A", content=response_a2))
        
        # Debater B (Closing)
        prompt_b2 = f"""Topic: {topic}
        
Debater A's Rebuttal:
{response_a2}

Produce your final rebuttal.
Start with 'FINAL_ANSWER: NO'."""
        
        response_b2 = debater_b.generate(prompt_b2)
        self.transcript.append(DebateTurn(speaker="Debater B", content=response_b2))
        
        # --- Judgment ---
        
        transcript_text = "\n\n".join([f"{t.speaker}: {t.content}" for t in self.transcript])
        
        prompt_judge = f"""Analyze the following debate transcript and decide the winner.

Topic: {topic}

Transcript:
{transcript_text}
"""
        
        response_judge = judge.generate(prompt_judge)
        
        # Parse Judge Output (JSON)
        try:
            # Clean up any markdown formatting if present (```json ... ```)
            cleaned_json = response_judge.replace("```json", "").replace("```", "").strip()
            verdict_data = json.loads(cleaned_json)
            
            winner = verdict_data.get("winner", "Unknown")
            confidence = verdict_data.get("confidence", 0)
            reason = verdict_data.get("reason", "No reason provided.")
            
        except json.JSONDecodeError:
            # Fallback parsing if JSON fails
            winner = "Error"
            confidence = 0
            reason = f"Failed to parse judge output: {response_judge}"

        return DebateResult(
            transcript=self.transcript,
            winner=winner,
            confidence=confidence,
            reason=reason
        )
