# usepolvo/tentacles/hubspot/tasks/schemas.py

from typing import Optional

from pydantic import BaseModel, Field


class CreateTask(BaseModel):
    hs_task_subject: str = Field(..., alias="title")
    hs_task_body: Optional[str] = Field(None, alias="description")
    hs_task_priority: Optional[str] = Field(None, alias="priority")
    hs_task_status: Optional[str] = Field(None, alias="status")
    hs_timestamp: Optional[int] = Field(None, alias="due_date")
    hubspot_owner_id: Optional[str] = Field(None, alias="owner_id")
