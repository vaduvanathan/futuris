import os
import google.generativeai as genai
from google.generativeai import types
from typing import List, Optional, Any

class Agent:
    def __init__(
        self, 
        name: str, 
        model: str, 
        system_instruction: str, 
        tools: Optional[List[Any]] = None,
        generation_config: Optional[Any] = None
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
            print(f"Warning: GOOGLE_API_KEY not found for agent {name}. Agent may fail to generate.")
            raise ValueError("GOOGLE_API_KEY not found. Please set it in the environment variables.")
            
        genai.configure(api_key=api_key)
        self.model_instance = genai.GenerativeModel(
            model_name=self.model,
            system_instruction=self.system_instruction,
            tools=self.tools
        )

    def generate(self, prompt: str, context: Optional[List[Any]] = None) -> str:
        """Generates a response from the agent."""
        
        try:
            response = self.model_instance.generate_content(
                prompt,
                generation_config=self.generation_config,
            )
            
            return response.text
        except Exception as e:
            return f"Error generating response for {self.name}: {str(e)}"
