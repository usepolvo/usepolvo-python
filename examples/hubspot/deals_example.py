import asyncio
from typing import Any, Dict

from usepolvo.tentacles.hubspot import HubSpotClient
from usepolvo.tentacles.hubspot.resources.deals.schemas import CreateDeal, UpdateDeal


def list_deals(client: HubSpotClient):
    """List deals with pagination."""
    deals = client.deals.list(limit=10)
    for deal in deals:
        print(f"Deal ID: {deal.id}")
        print(f"Email: {deal.properties.get('email')}")
        print("---")
    return deals


def get_deal(client: HubSpotClient, deal_id: str):
    """Get a single deal by ID."""
    deal = client.deals.get(deal_id)
    print(f"Deal ID: {deal.id}")
    print(f"Created: {deal.created_at}")
    print(f"Email: {deal.properties.get('email')}")
    print(f"Name: {deal.properties.get('firstname', '')} {deal.properties.get('lastname', '')}")
    return deal


def update_deal(client: HubSpotClient, deal_id: str, data: Dict[str, Any]):
    """Update an existing deal with schema validation."""
    # Validate update data using schema
    validated_data = UpdateDeal(properties=data)

    deal = client.deals.update(deal_id, validated_data.model_dump())
    print(f"Updated Deal ID: {deal.id}")
    print(f"Email: {deal.properties.get('email')}")
    return deal


async def main():
    # Initialize client with required scopes
    client = HubSpotClient(scopes=["crm.objects.deals.read", "crm.objects.deals.write"])

    # List existing deals
    print("Listing deals:")
    deals = list_deals(client)

    # Get specific deal if available
    if deals:
        first_deal = deals[0]
        print("\nGetting specific deal:")
        get_deal(client, first_deal.id)

        # Update the deal
        update_data = {"amount": "20000", "dealstage": "presentationscheduled"}
        print("\nUpdating deal:")
        update_deal(client, first_deal.id, update_data)


if __name__ == "__main__":
    asyncio.run(main())
