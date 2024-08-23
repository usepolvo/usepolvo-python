import asyncio

from usepolvo.tentacles.certn import CertnClient
from usepolvo.tentacles.certn.webhooks import CertnWebhook


def list_applications(client):
    applications = client.applications.list()
    if applications.count == 0:
        print("No applications found.")
    for application in applications.results:
        print(f"Application ID: {application.id}, Status: {application.status}")
    return applications


async def main():
    client = CertnClient()
    webhook = CertnWebhook()

    # Set the webhook secret key (if required)
    webhook.set_secret_key("your_certn_webhook_secret")

    # List applications
    list_applications(client)

    # Start the webhook server and keep it running
    await webhook.run("/certn", port=8080)


if __name__ == "__main__":
    asyncio.run(main())
