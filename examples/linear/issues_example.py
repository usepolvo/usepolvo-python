from usepolvo.tentacles.linear.client import LinearClient
from usepolvo.tentacles.linear.webhooks.handler import LinearWebhook

client = LinearClient()
webhook = LinearWebhook()


def list_issues():
    issues = client.issues.list()
    for issue in issues.nodes:
        print(f"Issue ID: {issue.id}, Title: {issue.title}")
    return issues


def get_issue(issue_id):
    issue = client.issues.get(issue_id)
    print(f"Issue ID: {issue.id}, Title: {issue.title}")


# Register your event handlers
@webhook.register("issue.update")
async def handle_update(payload):
    print(f"Update event: ID: {payload.data.id}, Title: {payload.data.title}")


async def main():
    issues = list_issues()
    issue_id = issues.nodes[0].id
    get_issue(issue_id)

    # Start the webhook server
    await webhook.run("/linear-webhook")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
