from enum import Enum
from typing import Annotated, Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, Field, HttpUrl, model_validator


class WebhookAction(str, Enum):
    CREATE = "create"
    UPDATE = "update"
    REMOVE = "remove"
    RESTORE = "restore"


class WebhookType(str, Enum):
    ISSUE = "Issue"
    COMMENT = "Comment"
    PROJECT = "Project"
    CYCLE = "Cycle"
    REACTION = "Reaction"
    ISSUE_LABEL = "IssueLabel"
    ISSUE_ATTACHMENT = "IssueAttachment"
    PROJECT_UPDATE = "ProjectUpdate"
    DOCUMENT = "Document"
    USER = "User"


class UserType(str, Enum):
    USER = "user"
    BOT = "bot"
    UNKNOWN = "unknown"


class StateType(str, Enum):
    TRIAGE = "triage"
    BACKLOG = "backlog"
    UNSTARTED = "unstarted"
    STARTED = "started"
    COMPLETED = "completed"
    CANCELED = "canceled"
    DUPLICATE = "duplicate"


# Base Models
class User(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    avatarUrl: Optional[HttpUrl] = None
    type: Optional[UserType] = None
    active: Optional[bool] = None
    displayName: Optional[str] = None
    organizationId: Optional[str] = None


class Label(BaseModel):
    id: Optional[str] = None
    color: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None


class Project(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    url: Optional[HttpUrl] = None
    description: Optional[str] = None
    createdAt: Optional[str] = None
    updatedAt: Optional[str] = None
    state: Optional[str] = None
    startDate: Optional[str] = None
    targetDate: Optional[str] = None


class State(BaseModel):
    id: Optional[str] = None
    color: Optional[str] = None
    name: Optional[str] = None
    type: Optional[StateType] = None
    position: Optional[float] = None


class Team(BaseModel):
    id: Optional[str] = None
    key: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None


class Attachment(BaseModel):
    id: Optional[str] = None
    title: Optional[str] = None
    url: Optional[HttpUrl] = None
    size: Optional[int] = None
    contentType: Optional[str] = None
    uploadUrl: Optional[HttpUrl] = None


# Common base class for all webhook data types
class BaseWebhookData(BaseModel):
    """Base class containing fields common to all webhook types"""

    id: str
    createdAt: str
    updatedAt: str
    type: WebhookType  # Discriminator field


# Event-specific Data Models
class CommonOptionalFields(BaseModel):
    """Common optional fields that appear in multiple event types"""

    number: Optional[int] = None
    title: Optional[str] = None
    priority: Optional[int] = None
    boardOrder: Optional[float] = None
    sortOrder: Optional[float] = None
    prioritySortOrder: Optional[float] = None
    startedAt: Optional[str] = None
    completedAt: Optional[str] = None
    slaType: Optional[str] = None
    addedToProjectAt: Optional[str] = None
    labelIds: Optional[List[str]] = None
    teamId: Optional[str] = None
    projectId: Optional[str] = None
    lastAppliedTemplateId: Optional[str] = None
    previousIdentifiers: Optional[List[str]] = None
    creatorId: Optional[str] = None
    assigneeId: Optional[str] = None
    stateId: Optional[str] = None
    reactionData: Optional[List[Dict[str, Any]]] = None
    priorityLabel: Optional[str] = None
    botActor: Optional[User] = None
    identifier: Optional[str] = None
    url: Optional[HttpUrl] = None
    subscriberIds: Optional[List[str]] = None
    assignee: Optional[User] = None
    project: Optional[Project] = None
    state: Optional[State] = None
    team: Optional[Team] = None
    labels: Optional[List[Label]] = None
    description: Optional[str] = None
    descriptionData: Optional[str] = None


class IssueData(BaseWebhookData, CommonOptionalFields):
    """Issue-specific webhook data"""

    type: Literal[WebhookType.ISSUE]


class CommentData(BaseWebhookData, CommonOptionalFields):
    """Comment-specific webhook data"""

    type: Literal[WebhookType.COMMENT]
    body: Optional[str] = None
    userId: Optional[str] = None
    issueId: Optional[str] = None
    bodyData: Optional[str] = None


class IssueLabelData(BaseWebhookData, CommonOptionalFields):
    """IssueLabel-specific webhook data"""

    type: Literal[WebhookType.ISSUE_LABEL]


class IssueAttachmentData(BaseWebhookData):
    """IssueAttachment-specific webhook data"""

    type: Literal[WebhookType.ISSUE_ATTACHMENT]
    issueId: Optional[str] = None
    attachment: Optional[Attachment] = None


class ProjectData(BaseWebhookData):
    """Project-specific webhook data"""

    type: Literal[WebhookType.PROJECT]
    name: Optional[str] = None
    description: Optional[str] = None
    teamId: Optional[str] = None
    state: Optional[str] = None
    startDate: Optional[str] = None
    targetDate: Optional[str] = None
    lead: Optional[User] = None


class ProjectUpdateData(BaseWebhookData):
    """ProjectUpdate-specific webhook data"""

    type: Literal[WebhookType.PROJECT_UPDATE]
    projectId: Optional[str] = None
    userId: Optional[str] = None
    body: Optional[str] = None
    bodyData: Optional[str] = None


class CycleData(BaseWebhookData):
    """Cycle-specific webhook data"""

    type: Literal[WebhookType.CYCLE]
    name: Optional[str] = None
    number: Optional[int] = None
    teamId: Optional[str] = None
    startDate: Optional[str] = None
    endDate: Optional[str] = None


class ReactionData(BaseWebhookData):
    """Reaction-specific webhook data"""

    type: Literal[WebhookType.REACTION]
    emoji: Optional[str] = None
    userId: Optional[str] = None
    commentId: Optional[str] = None
    issueId: Optional[str] = None


class DocumentData(BaseWebhookData):
    """Document-specific webhook data"""

    type: Literal[WebhookType.DOCUMENT]
    title: Optional[str] = None
    content: Optional[str] = None
    contentData: Optional[str] = None
    icon: Optional[str] = None
    organizationId: Optional[str] = None


class UserData(BaseWebhookData):
    """User-specific webhook data"""

    type: Literal[WebhookType.USER]
    name: Optional[str] = None
    email: Optional[str] = None
    active: Optional[bool] = None
    displayName: Optional[str] = None
    organizationId: Optional[str] = None
    avatarUrl: Optional[HttpUrl] = None


# Discriminated union of all possible webhook data types
WebhookData = Annotated[
    Union[
        IssueData,
        CommentData,
        IssueLabelData,
        IssueAttachmentData,
        ProjectData,
        ProjectUpdateData,
        CycleData,
        ReactionData,
        DocumentData,
        UserData,
    ],
    Field(discriminator="type"),
]


class UpdatedFromData(BaseModel):
    """Represents the partial data in updatedFrom field"""

    updatedAt: Optional[str] = None
    sortOrder: Optional[float] = None
    prioritySortOrder: Optional[float] = None
    completedAt: Optional[str] = None
    stateId: Optional[str] = None
    assigneeId: Optional[str] = None
    priority: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    teamId: Optional[str] = None


class LinearWebhookPayload(BaseModel):
    """Main webhook payload model"""

    action: WebhookAction
    type: WebhookType
    data: WebhookData
    actor: Optional[User] = None
    createdAt: Optional[str] = None
    updatedFrom: Optional[UpdatedFromData] = None
    url: Optional[HttpUrl] = None
    organizationId: str
    webhookTimestamp: int
    webhookId: str

    @model_validator(mode="before")
    @classmethod
    def inherit_webhook_type(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Ensures the type field is properly inherited by the data object"""
        if isinstance(values, dict):
            webhook_type = values.get("type")
            if webhook_type and "data" in values and isinstance(values["data"], dict):
                # Inherit the type from the parent webhook
                values["data"]["type"] = webhook_type
        return values

    def get_event_type(self) -> str:
        """Returns event type in format 'type.action' (e.g., 'issue.update')"""
        return f"{self.type.lower()}.{self.action.value}"

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LinearWebhookPayload":
        """Helper method to create instance from dictionary"""
        # Ensure the type field is added to the data for discrimination
        if "data" in data and "type" in data:
            data["data"]["type"] = data["type"]
        return cls(**data)

    def get_identifier(self) -> str:
        """Returns the unique identifier for the webhook data"""
        if isinstance(self.data, IssueData) and self.data.identifier:
            return self.data.identifier
        return self.data.id


# Example usage:
"""
# Parse a webhook payload
payload = LinearWebhookPayload.from_dict({
    "action": "create",
    "type": "IssueAttachment",
    "data": {
        "id": "123",
        "createdAt": "2025-01-17T16:57:04.664Z",
        "updatedAt": "2025-01-17T16:57:04.664Z",
        "issueId": "issue-123",
        "attachment": {
            "title": "Screenshot.png",
            "url": "https://example.com/files/screenshot.png"
        }
    },
    "organizationId": "org-123",
    "webhookTimestamp": 1737133024760,
    "webhookId": "webhook-123"
})

# Type-safe access to data
if isinstance(payload.data, IssueAttachmentData):
    print(f"Attachment title: {payload.data.attachment.title}")
elif isinstance(payload.data, DocumentData):
    print(f"Document title: {payload.data.title}")
"""
