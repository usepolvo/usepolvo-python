# usepolvo/tentacles/hubspot/notes/schemas.py

from typing import List, Optional

from pydantic import BaseModel, Field


class Association(BaseModel):
    to: Dict[str, str]
    types: List[Dict[str, str]]


class CreateNote(BaseModel):
    hs_note_body: str = Field(..., alias="content")
    hubspot_owner_id: Optional[str] = Field(None, alias="owner_id")
    hs_timestamp: Optional[int] = Field(None, alias="timestamp")
    associations: Optional[List[Association]] = None
