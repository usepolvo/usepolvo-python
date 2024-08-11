from usepolvo.tentacles.certn import CertnClient, CertnWebhook
import asyncio

client = CertnClient()
webhook = CertnWebhook()


async def list_applications():
    applications = await client.applications.list()
    if applications.count == 0:
        print("No applications found.")
    for application in applications.results:
        print(f"Application ID: {application.id}, Status: {application.status}")
    return applications


@webhook.register("application.created")
async def handle_application_created(payload):
    application_id = payload["data"]["id"]
    print(f"New application created with ID: {application_id}")
    application = await client.applications.get(application_id)
    print(f"Application status: {application.status}")


@webhook.register("application.updated")
async def handle_application_updated(payload):
    application_id = payload["data"]["id"]
    print(f"Application updated with ID: {application_id}")
    application = await client.applications.get(application_id)
    print(f"Updated application status: {application.status}")


async def main():
    # Start the webhook server
    await webhook.start_server("/webhook/certn", port=8080)

    # List applications
    await list_applications()

    # Keep the server running
    while True:
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
