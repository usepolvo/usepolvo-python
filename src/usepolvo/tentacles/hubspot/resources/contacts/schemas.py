from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator


class Contact(BaseModel):
    id: Optional[str] = None
    email: Optional[EmailStr] = None
    firstname: Optional[str] = Field(None, alias="first_name")
    lastname: Optional[str] = Field(None, alias="last_name")
    phone: Optional[str] = None

    @field_validator("phone")
    def validate_phone(cls, value):
        if value and not value.replace("+", "").isdigit():
            raise ValueError("Phone number must contain only digits and optionally a '+' at the start")
        return value

    @model_validator(mode="before")
    def check_name_or_email(cls, values):
        firstname, lastname, email = values.get("firstname"), values.get("lastname"), values.get("email")
        if not any([firstname, lastname, email]):
            raise ValueError("At least one of first name, last name, or email must be provided")
        return values


class CreateContact(Contact):
    email: EmailStr
