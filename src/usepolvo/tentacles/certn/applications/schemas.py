# usepolvo/tentacles/certn/applications/schemas.py

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, HttpUrl


class Applicant(BaseModel):
    id: str
    status: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    application_url: Optional[HttpUrl] = None
    report_url: HttpUrl
    employer_references_min: int


class Application(BaseModel):
    created: datetime
    modified: datetime
    id: str
    applicant: Applicant
    is_active: bool
    is_selected: bool
    team_id: str


class EnhancedIdentityVerification(BaseModel):
    dispute: bool
    status: str
    status_label: str


class ReportSummary(BaseModel):
    enhanced_identity_verification: EnhancedIdentityVerification
    report_result: str
    report_result_label: str
    dispute: bool
    report_status: str
    report_status_label: str


class ApplicationResponse(BaseModel):
    created: datetime
    modified: datetime
    last_updated: datetime
    submitted_time: Optional[datetime]
    id: str
    short_uid: str
    is_submitted: bool
    applicant_type: str
    result: str
    result_label: str
    report_status: str
    country: str
    order_status: str
    information: Dict[str, Any]
    application: Application
    report_summary: ReportSummary
    status: str
    status_label: str


class ApplicationListResponse(BaseModel):
    count: int
    next: Optional[HttpUrl] = None
    previous: Optional[HttpUrl] = None
    results: List[ApplicationResponse]
