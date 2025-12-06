
import os
from google import genai
from google.genai import types
from app.agents.core import Agent
from app.agents.schemas import DebateVerdict

# Define Debater A (Proponent)
debater_a = Agent(
    name="Debater A",
    model="gemini-3-pro-preview",
    system_instruction="""You are Debater A in a formal debate.
Your role is to argue YES (the Proponent) for the given topic.
- Your arguments must be constructive, logical, and evidence-based.
- Use the 'google_search' tool to find real-world facts and citations.
- Start your response with 'FINAL_ANSWER: YES' followed by your argument.
- Keep your response under 500 words.
""",
    tools=[{"google_search": {}}],
    # Enable high thinking level for deep reasoning
    generation_config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_level="high")
    )
)

# Define Debater B (Opponent)
debater_b = Agent(
    name="Debater B",
    model="gemini-2.5-flash",
    system_instruction="""You are Debater B in a formal debate.
Your role is to argue NO (the Opponent) against the given topic.
- Your goal is to critique Debater A's arguments and provide counter-evidence.
- Use the 'google_search' tool to find contradictions or alternative facts.
- Start your response with 'FINAL_ANSWER: NO' followed by your counter-argument.
- Keep your response under 500 words.
""",
    tools=[{"google_search": {}}],
    # Standard config for the faster model
)

# Define Judge
judge = Agent(
    name="Judge",
    model="gemini-3-pro-preview",
    system_instruction="""You are a neutral Judge in a formal debate.
Your task is to analyze the full transcript of the debate and decide the winner.
- You must be objective and base your decision ONLY on the arguments presented.
- You will receive the full transcript of the debate.
- Output your verdict in strict JSON format.
""",
    generation_config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_level="high"),
        response_mime_type="application/json",
        response_schema=DebateVerdict
    )
)
