# hubspot_tasks_example.py

import asyncio
import time

from usepolvo.tentacles.hubspot import HubSpotClient


def create_task(client: HubSpotClient, data):
    task = client.tasks.create(data)
    print(f"Created Task ID: {task.id}, Subject: {task.properties.get('hs_task_subject', '')}")
    return task


async def main():
    client = HubSpotClient()

    # Create a new task
    new_task_data = {
        "properties": {
            "title": "Follow up with lead",
            "description": "Discuss product features and pricing",
            "priority": "HIGH",
            "status": "NOT_STARTED",
            "type": "CALL",
            "owner_id": "1234",
        },
        "associations": [{"to": {"id": "1234"}, "types": [{"category": "HUBSPOT_DEFINED", "id": "204"}]}],
    }
    create_task(client, new_task_data)


if __name__ == "__main__":
    asyncio.run(main())
