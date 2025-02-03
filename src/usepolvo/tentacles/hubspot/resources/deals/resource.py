from typing import Any, Dict, List, Optional

from usepolvo.arms.base_resource import BaseResource
from usepolvo.beak.exceptions import ResourceNotFoundError, ValidationError
from usepolvo.tentacles.hubspot.resources.deals.schemas import (
    CreateDeal,
    Deal,
    UpdateDeal,
)


class DealResource(BaseResource):
    def __init__(self, client):
        super().__init__(client)
        self.base_path = "deals"

    def list(self, limit: int = 10, after: Optional[str] = None) -> List[Deal]:
        """List deals with pagination."""
        try:
            params = self.client.get_pagination_params(limit=limit, after=after)
            response = self.client.rate_limited_execute(
                lambda: self.client.client.crm.deals.basic_api.get_page(**params)
            )
            return [Deal(**deal.to_dict()) for deal in response.results]
        except Exception as e:
            self.client.handle_error(e)

    def get(self, deal_id: str) -> Deal:
        """Get a single deal by ID."""
        try:
            response = self.client.rate_limited_execute(
                lambda: self.client.client.crm.deals.basic_api.get_by_id(deal_id)
            )
            return Deal(**response.to_dict())
        except ResourceNotFoundError:
            raise ResourceNotFoundError(f"Deal with ID {deal_id} not found")

    def create(self, data: Dict[str, Any]) -> Deal:
        """Create a new deal."""
        try:
            # Validate input data
            validated_data = CreateDeal(**data)

            # Create deal using HubSpot SDK
            response = self.client.rate_limited_execute(
                lambda: self.client.client.crm.deals.basic_api.create(
                    simple_public_object_input_for_create=validated_data.model_dump(exclude_none=True)
                )
            )
            return Deal(**response.to_dict())
        except ValidationError as e:
            raise ValidationError(f"Invalid data for creating deal: {str(e)}")

    def update(self, deal_id: str, data: Dict[str, Any]) -> Deal:
        """Update an existing deal."""
        try:
            # Validate update data
            validated_data = UpdateDeal(**data)

            # Update deal using HubSpot SDK
            response = self.client.rate_limited_execute(
                lambda: self.client.client.crm.deals.basic_api.update(
                    deal_id=deal_id, simple_public_object_input=validated_data.dict(exclude_unset=True)
                )
            )
            return Deal(**response.to_dict())
        except ResourceNotFoundError:
            raise ResourceNotFoundError(f"Deal with ID {deal_id} not found")
        except ValidationError as e:
            raise ValidationError(f"Invalid data for updating deal: {str(e)}")

    def delete(self, deal_id: str) -> None:
        """Delete a deal."""
        try:
            self.client.rate_limited_execute(lambda: self.client.client.crm.deals.basic_api.archive(deal_id))
        except ResourceNotFoundError:
            raise ResourceNotFoundError(f"Deal with ID {deal_id} not found")
