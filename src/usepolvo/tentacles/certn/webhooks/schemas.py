from typing import Any, Dict

from pydantic import BaseModel


class CertnWebhookPayload(BaseModel):
    created: str
    modified: str
    last_updated: str
    submitted_time: str
    request_identity_verification: bool = False
    request_equifax: bool = False
    request_base: bool = False
    request_instant_verify_employment: bool = False
    request_instant_verify_education: bool = False
    request_instant_verify_credential: bool = False
    request_international_criminal_record_check: bool = False
    request_enhanced_identity_verification: bool = False
    request_motor_vehicle_records: bool = False
    request_criminal_record_check: bool = False
    request_enhanced_criminal_record_check: bool = False
    request_vulnerable_sector_criminal_record_check: bool = False
    request_employer_references: bool = False
    request_address_references: bool = False
    request_employer_phone_references: bool = False
    request_address_phone_references: bool = False
    request_softcheck: bool = False
    request_social_media_check: bool = False
    request_soquij: bool = False
    request_us_criminal_record_check_tier_1: bool = False
    request_us_criminal_record_check_tier_2: bool = False
    request_us_criminal_record_check_tier_3: bool = False
    request_education_verification: bool = False
    request_credential_verification: bool = False
    request_employment_verification: bool = False
    request_vaccination_check: bool = False
    request_australian_criminal_intelligence_commission_check: bool = False
    request_right_to_work: bool = False
    request_uk_basic_dbs_check: bool = False
    request_uk_basic_ds_check: bool = False
    request_uk_right_to_work_check: bool = False

    def get_event_type(self) -> str:
        for field, value in self.model_dump().items():
            if field.startswith("request_") and value is True:
                return field
        return "unknown"

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CertnWebhookPayload":
        return cls(**data)
