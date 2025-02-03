# usepolvo/tentacles/hubspot/tasks/schemas.py

from datetime import datetime, timezone
from functools import partial
from typing import Annotated, List, Optional

from pydantic import BaseModel, Field, PlainSerializer

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
    hs_timestamp: CustomDateTime = Field(default_factory=partial(datetime.now, tz=timezone.utc), alias="timestamp")
    hs_task_subject: str = Field(..., alias="title")
    hs_task_body: Optional[str] = Field(None, alias="description")
    hs_task_priority: Optional[str] = Field(None, alias="priority")
    hs_task_status: Optional[str] = Field(None, alias="status")
    hs_task_type: Optional[str] = Field(None, alias="type")
    hubspot_owner_id: Optional[str] = Field(None, alias="owner_id")


class CreateTask(BaseModel):
    properties: Properties
    associations: List[Association]
