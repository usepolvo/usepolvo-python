from typing import List, Optional

from pydantic import BaseModel, Field


class CompletionRequest(BaseModel):
    model: str = Field(default="text-davinci-002")
    prompt: str
    max_tokens: int = Field(default=100, ge=1, le=4096)
    temperature: float = Field(default=0.7, ge=0, le=1)
    n: int = Field(default=1, ge=1)
    stop: Optional[List[str]] = None


class Choice(BaseModel):
    text: str
    index: int
    logprobs: Optional[Any] = None
    finish_reason: str


class CompletionResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: List[Choice]
