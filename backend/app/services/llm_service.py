from openai import AsyncOpenAI
from typing import Dict, Any, List, Optional
from loguru import logger

class LLMService:
    """
    Service for handling interactions with LLM models like OpenAI.
    """
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the LLM service with optional API key."""
        self.client = AsyncOpenAI(api_key=api_key) if api_key else AsyncOpenAI()
    
    async def generate_completion(self, prompt: str, model: str = "gpt-4-turbo", **kwargs) -> str:
        """
        Generate a text completion using the specified LLM model.
        
        Args:
            prompt: The input prompt or user message
            model: The model to use (default: gpt-4-turbo)
            **kwargs: Additional parameters to pass to the completion API
            
        Returns:
            The generated text completion
        """
        try:
            response = await self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                **kwargs
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating completion: {e}")
            return f"Error: {str(e)}"

# ... dentro do _build_system_prompt string ...
# CONTEXT PROVIDED TO YOU (in user message, under "--- Start of Additional Context ---"):
# ... outros campos ...
# - `form_submission`: (Optional) If present, this request is a response to a form you previously requested.
#     - `form_id`: The ID of the form that was submitted.

#     - YOUR TASK: Use `form_submission.. to populate the `entities` for the original `intent` that required clarification. Then proceed as if you have all entities.
# ... resto do prompt ...