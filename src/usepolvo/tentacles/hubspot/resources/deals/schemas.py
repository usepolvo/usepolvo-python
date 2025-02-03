from datetime import datetime
from typing import Any, Dict

from pydantic import BaseModel, Field, field_validator, model_validator


class BaseDeal(BaseModel):
    """Base schema with common deal fields and validations."""

    properties: Dict[str, Any] = Field(default_factory=dict)

    @field_validator("properties")
    def validate_phone(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        if phone := values.get("phone"):
            if not str(phone).replace("+", "").isdigit():
                raise ValueError("Phone number must contain only digits and optionally a '+' at the start")
        return values

    @field_validator("properties")
    def validate_amount(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        if amount := values.get("amount"):
            if float(amount) < 0:
                raise ValueError("Amount must be non-negative")
        return values


class CreateDeal(BaseDeal):
    """Schema for creating a new deal."""

    pass


class UpdateDeal(BaseDeal):
    """Schema for updating an existing deal. All fields optional."""

    pass


class Deal(BaseDeal):
    """Schema for deal responses from the API."""

    id: str
    properties: Dict[str, Any]
    created_at: datetime = Field(alias="createdAat")
    updated_at: datetime = Field(alias="updatedAt")
    archived: bool = False

    class Config:
        from_attributes = True  # Allows conversion from ORM objects
        populate_by_name = True  # Allows using both camelCase and snake_case
