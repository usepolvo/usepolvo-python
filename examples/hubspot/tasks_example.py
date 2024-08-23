# hubspot_tasks_example.py

import asyncio
import time

from usepolvo.tentacles.hubspot import HubSpotClient


def create_task(client, data):
    task = client.tasks.create(data)
    print(f"Created Task ID: {task.id}, Subject: {task.properties.get('hs_task_subject', '')}")
    return task


async def main():
    client = HubSpotClient()

    # Create a new task
    new_task_data = {
        "title": "Follow up with lead",
        "description": "Discuss product features and pricing",
        "priority": "HIGH",
        "status": "NOT_STARTED",
        "due_date": int(time.time()) + 86400,  # Due tomorrow
        "owner_id": "12345",  # Replace with actual owner ID
    }
    create_task(client, new_task_data)


if __name__ == "__main__":
    asyncio.run(main())
