# salesforce_example.py

import asyncio

from usepolvo.tentacles.salesforce import SalesforceClient


def list_accounts(client):
    accounts = client.accounts.list()
    for account in accounts.recentItems:
        print(f"Account ID: {account.Id}, Name: {account.Name}")
    return accounts.recentItems  # Return the list of recent items


def get_account(client, account_id):
    account = client.accounts.get(account_id)
    print(f"Account ID: {account.Id}, Name: {account.Name}")
    return account


async def main():
    client = SalesforceClient()

    # List accounts
    accounts = list_accounts(client)

    # Get the first account if available
    if accounts:
        first_account = accounts[0]
        get_account(client, first_account.Id)
    else:
        print("No accounts found.")


if __name__ == "__main__":
    asyncio.run(main())
