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
    title: str
    description: str | None
    state: IssueState
    assignee: IssueAssignee | None


class IssueListResponse(BaseModel):
    nodes: List[Issue]
    pageInfo: Dict[str, Any]
