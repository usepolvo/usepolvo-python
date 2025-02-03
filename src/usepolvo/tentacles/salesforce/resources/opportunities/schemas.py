from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, HttpUrl


class OpportunityAttributes(BaseModel):
    type: str
    url: str


class Opportunity(BaseModel):
    attributes: OpportunityAttributes
    Id: str
    Name: str


class OpportunityUrls(BaseModel):
    compactLayouts: str
    rowTemplate: str
    approvalLayouts: str
    listviews: str
    describe: str
    quickActions: str
    layouts: str
    sobject: str


class ObjectDescribe(BaseModel):
    activateable: bool
    associateEntityType: Optional[str] = None
    associateParentEntity: Optional[str] = None
    createable: bool
    custom: bool
    customSetting: bool
    deepCloneable: bool
    deletable: bool
    deprecatedAndHidden: bool
    feedEnabled: bool
    hasSubtypes: bool
    isInterface: bool
    isSubtype: bool
    keyPrefix: str
    label: str
    labelPlural: str
    layoutable: bool
    mergeable: bool
    mruEnabled: bool
    name: str
    queryable: bool
    replicateable: bool
    retrieveable: bool
    searchable: bool
    triggerable: bool
    undeletable: bool
    updateable: bool
    urls: OpportunityUrls


class OpportunityListResponse(BaseModel):
    objectDescribe: ObjectDescribe
    recentItems: List[Opportunity]


class OpportunityResponse(BaseModel):
    Id: str
    Name: str
    Type: Optional[str] = None
    Industry: Optional[str] = None
    Rating: Optional[str] = None
    Phone: Optional[str] = None
    Website: Optional[HttpUrl] = None
    AnnualRevenue: Optional[float] = None
    NumberOfEmployees: Optional[int] = None
    Description: Optional[str] = None
    attributes: OpportunityAttributes


class OpportunityResponse(BaseModel):
    attributes: Optional[OpportunityAttributes] = None
    Id: Optional[str] = None
    IsDeleted: Optional[bool] = None
    MasterRecordId: Optional[Any] = None
    Name: Optional[str] = None
    Type: Optional[Any] = None
    ParentId: Optional[Any] = None
    BillingStreet: Optional[Any] = None
    BillingCity: Optional[Any] = None
    BillingState: Optional[Any] = None
    BillingPostalCode: Optional[Any] = None
    BillingCountry: Optional[Any] = None
    BillingLatitude: Optional[Any] = None
    BillingLongitude: Optional[Any] = None
    BillingGeocodeAccuracy: Optional[Any] = None
    BillingAddress: Optional[Any] = None
    ShippingStreet: Optional[Any] = None
    ShippingCity: Optional[Any] = None
    ShippingState: Optional[Any] = None
    ShippingPostalCode: Optional[Any] = None
    ShippingCountry: Optional[Any] = None
    ShippingLatitude: Optional[Any] = None
    ShippingLongitude: Optional[Any] = None
    ShippingGeocodeAccuracy: Optional[Any] = None
    ShippingAddress: Optional[Any] = None
    Phone: Optional[Any] = None
    Fax: Optional[Any] = None
    OpportunityNumber: Optional[Any] = None
    Website: Optional[Any] = None
    PhotoUrl: Optional[str] = None
    Sic: Optional[Any] = None
    Industry: Optional[Any] = None
    AnnualRevenue: Optional[Any] = None
    NumberOfEmployees: Optional[Any] = None
    Ownership: Optional[Any] = None
    TickerSymbol: Optional[Any] = None
    Description: Optional[Any] = None
    Rating: Optional[Any] = None
    Site: Optional[Any] = None
    OwnerId: Optional[str] = None
    CreatedDate: Optional[str] = None
    CreatedById: Optional[str] = None
    LastModifiedDate: Optional[str] = None
    LastModifiedById: Optional[str] = None
    SystemModstamp: Optional[str] = None
    LastActivityDate: Optional[Any] = None
    LastViewedDate: Optional[str] = None
    LastReferencedDate: Optional[str] = None
    Jigsaw: Optional[Any] = None
    JigsawCompanyId: Optional[Any] = None
    CleanStatus: Optional[str] = None
    OpportunitySource: Optional[Any] = None
    DunsNumber: Optional[Any] = None
    Tradestyle: Optional[Any] = None
    NaicsCode: Optional[Any] = None
    NaicsDesc: Optional[Any] = None
    YearStarted: Optional[Any] = None
    SicDesc: Optional[Any] = None
    DandbCompanyId: Optional[Any] = None
    OperatingHoursId: Optional[Any] = None
