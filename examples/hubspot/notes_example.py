# hubspot_notes_example.py

import asyncio

from usepolvo.tentacles.hubspot import HubSpotClient


def create_note(client, data):
    note = client.notes.create(data)
    print(f"Created Note ID: {note.id}, Content: {note.properties.get('hs_note_body', '')[:50]}...")
    return note


async def main():
    client = HubSpotClient()

    # Create a new note
    new_note_data = {
        "content": "Had a great conversation with the lead. They're interested in our premium package and would like a demo next week.",
        "owner_id": "12345",  # Replace with actual owner ID
        "associations": [
            {
                "to": {"id": "67890"},  # Replace with actual contact ID
                "types": [{"category": "CONTACT", "typeId": "contact_to_note"}],
            }
        ],
    }
    create_note(client, new_note_data)


if __name__ == "__main__":
    asyncio.run(main())
