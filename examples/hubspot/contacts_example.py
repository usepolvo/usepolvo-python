# hubspot_contacts_example.py

import asyncio

from usepolvo.tentacles.hubspot import HubSpotClient


def list_contacts(client: HubSpotClient):
    contacts = client.contacts.list(limit=10)
    for contact in contacts:
        print(
            f"Contact ID: {contact.id}, Name: {contact.properties.get('firstname', '')} {contact.properties.get('lastname', '')}"
        )
    return contacts


def get_contact(client: HubSpotClient, contact_id):
    contact = client.contacts.get(contact_id)
    print(
        f"Contact ID: {contact.id}, Name: {contact.properties.get('firstname', '')} {contact.properties.get('lastname', '')}"
    )
    return contact


def create_contact(client: HubSpotClient, data):
    contact = client.contacts.create(data)
    print(f"Created Contact ID: {contact.id}, Email: {contact.properties.get('email', '')}")
    return contact


def update_contact(client: HubSpotClient, contact_id, data):
    contact = client.contacts.update(contact_id, data)
    print(f"Updated Contact ID: {contact.id}, Email: {contact.properties.get('email', '')}")
    return contact


async def main():
    client = HubSpotClient()

    # List contacts
    contacts = list_contacts(client)

    # Get the first contact if available
    if contacts:
        first_contact = contacts[0]
        get_contact(client, first_contact.id)
    else:
        print("No contacts found.")

    # Create a new contact
    new_contact_data = {"email": "john.doe@example.com", "firstname": "John", "lastname": "Doe", "phone": "+1234567890"}
    create_contact(client, new_contact_data)

    # Update first contact if available
    updated_contact_data = {
        "lead_score": 100,
        "lead_insights": "Highly interested in our products",
    }
    update_contact(client, first_contact.id, updated_contact_data)


if __name__ == "__main__":
    asyncio.run(main())
