from typing import Optional

from pydantic import BaseModel, Field


class CompletionRequest(BaseModel):
    model: str = Field(default="gemini-pro")
    prompt: str
    max_output_tokens: Optional[int] = Field(default=None, ge=1, le=2048)
    temperature: Optional[float] = Field(default=None, ge=0, le=1)
    top_p: Optional[float] = Field(default=None, ge=0, le=1)
    top_k: Optional[int] = Field(default=None, ge=1)


class CompletionResponse(BaseModel):
    text: str
