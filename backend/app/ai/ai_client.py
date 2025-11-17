import os
from typing import Any, Dict
from ..core.config import settings

class AIClient:
    def __init__(self):
        self.provider = settings.LLM_PROVIDER
        # Initialize provider-specific clients (OpenAI, etc.)

    async def call(self, prompt: str, max_tokens: int = 512) -> Dict[str, Any]:
        # Simple abstraction — in production implement provider selection
        if self.provider == "openai":
            # use OPENAI_API_KEY and call OpenAI's API
            return {"text": "(simulated) response for prompt"}
        else:
            # fallback local model or simulated
            return {"text": "(local fallback) response"}

    async def ats_score(self, resume_text: str, job_text: str) -> Dict[str, Any]:
        prompt = f"Score this resume against job description and list missing keywords:\nJob:\n{job_text}\nResume:\n{resume_text}"
        return await self.call(prompt)

ai_client = AIClient()
