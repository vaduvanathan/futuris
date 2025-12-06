import os
from google import genai
from google.genai import types
from typing import List, Optional, Any

class Agent:
    def __init__(
        self, 
        name: str, 
        model: str, 
        system_instruction: str, 
        tools: Optional[List[Any]] = None,
        generation_config: Optional[types.GenerateContentConfig] = None
    ):
        self.name = name
        self.model = model
        self.system_instruction = system_instruction
        self.tools = tools
        self.generation_config = generation_config
        
        # Initialize the client
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            # Fallback: try loading .env if not already loaded
            from dotenv import load_dotenv
            load_dotenv()
            api_key = os.environ.get("GOOGLE_API_KEY")
            
        if not api_key:
            # Fallback to provided key if environment variable fails
            api_key = "AIzaSyAL8-S0eT9lxPi8jYngDkNF7GKEfZ58r7U"
            print(f"Warning: GOOGLE_API_KEY not found in env. Using fallback key for agent {name}.")
            
        if not api_key:
            print(f"Warning: GOOGLE_API_KEY not found for agent {name}. Agent may fail to generate.")
            
        self.client = genai.Client(api_key=api_key)

    def generate(self, prompt: str, context: Optional[List[Any]] = None) -> str:
        """Generates a response from the agent."""
        
        # If we have a chat history/context, we might want to use it, 
        # but for this strict debate protocol, we often pass the full transcript as the prompt 
        # or use a fresh context to avoid 'memory drift' between turns if we want strict adherence.
        # However, Gemini 3 handles context well.
        
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=self.generation_config,
            )
            
            # Handle structured output (Judge)
            if self.generation_config and self.generation_config.response_schema:
                # For structured output, the SDK might return a parsed object or we access .text
                # With the new SDK, if response_schema is set, .parsed might be available
                # but .text is always safe to return for now.
                return response.text
                
            return response.text
        except Exception as e:
            return f"Error generating response for {self.name}: {str(e)}"
