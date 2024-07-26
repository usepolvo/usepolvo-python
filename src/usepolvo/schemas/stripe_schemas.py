from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator


class Customer(BaseModel):
    id: Optional[str]
    email: EmailStr
    name: Optional[str]
    phone: Optional[str]
    created_at: Optional[datetime] = Field(default_factory=datetime.now)

    @field_validator("phone")
    def validate_phone(cls, value):
        if value and not value.isdigit():
            raise ValueError("Phone number must contain only digits")
        return value

    @model_validator(mode="wrap")
    def check_name_or_email(cls, values):
        name, email = values.get("name"), values.get("email")
        if not name and not email:
            raise ValueError("Either name or email must be provided")
        return values
