from pydantic import BaseModel, Field, field_validator


class CompletionRequest(BaseModel):
    prompt: str
    model: str = Field(default="claude-2")
    max_tokens_to_sample: int = Field(default=1000, ge=1, le=100000)
    temperature: float = Field(default=0.7, ge=0, le=1)

    @field_validator("prompt")
    def append_to_prompt(cls, v):
        if not v.startswith("\n\nHuman:"):
            v = f"\n\nHuman: {v}"
        if not v.endswith("\n\nAssistant:"):
            v = f"{v}\n\nAssistant:"
        return v


class CompletionResponse(BaseModel):
    completion: str
    stop_reason: str
    model: str
