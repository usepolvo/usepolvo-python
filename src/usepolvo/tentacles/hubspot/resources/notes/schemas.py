# usepolvo/tentacles/hubspot/notes/schemas.py

import time
from datetime import datetime, timezone
from functools import partial
from typing import Annotated, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field, PlainSerializer

CustomDateTime = Annotated[
    datetime,
    PlainSerializer(lambda _datetime: int(_datetime.timestamp() * 1000), return_type=str),
]


class AssociationType(BaseModel):
    associationCategory: str = Field(..., alias="category")
    associationTypeId: str = Field(..., alias="id")


class AssociationTo(BaseModel):
    id: str


class Association(BaseModel):
    to: AssociationTo
    types: List[AssociationType]


class Properties(BaseModel):
    hs_note_body: str = Field(..., alias="content")
    hs_timestamp: CustomDateTime = Field(default_factory=partial(datetime.now, tz=timezone.utc), alias="timestamp")
    hubspot_owner_id: Optional[int] = Field(None, alias="owner_id")
    hs_attachment_ids: Optional[str] = Field(None, alias="attachment_ids")


class CreateNote(BaseModel):
    properties: Properties
    associations: List[Association]
