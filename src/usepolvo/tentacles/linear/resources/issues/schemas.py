from typing import Any, Dict, List

from pydantic import BaseModel


class IssueState(BaseModel):
    id: str
    name: str


class IssueAssignee(BaseModel):
    id: str
    name: str


class Issue(BaseModel):
    id: str
    title: str | None = None
    description: str | None = None
    state: IssueState | None = None
    assignee: IssueAssignee | None = None


class IssueListResponse(BaseModel):
    nodes: List[Issue]
    pageInfo: Dict[str, Any]
