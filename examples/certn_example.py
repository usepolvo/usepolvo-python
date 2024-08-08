from usepolvo.tentacles.certn import CertnClient

client = CertnClient()


def list_applications():
    applications = client.applications.list()
    if applications.count == 0:
        print("No applications found.")
    for application in applications.results:
        print(f"Application ID: {application.id}, Status: {application.status}")
    return applications


if __name__ == "__main__":
    list_applications()
