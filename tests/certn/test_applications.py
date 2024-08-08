from unittest.mock import patch


def test_create_application(certn_application_resource):
    with patch.object(
        certn_application_resource, "create", return_value={"id": "app_123", "status": "created"}
    ) as mock_create:
        application = certn_application_resource.create(data={"name": "Test Applicant"})
        assert application["status"] == "created"
        mock_create.assert_called_once_with({"name": "Test Applicant"})


def test_list_applications(certn_application_resource):
    with patch.object(certn_application_resource, "list", return_value=[{"id": "app_123"}]) as mock_list:
        applications = certn_application_resource.list(page=1, size=10)
        assert isinstance(applications, list)
        assert applications[0]["id"] == "app_123"
        mock_list.assert_called_once()


def test_get_application(certn_application_resource):
    with patch.object(certn_application_resource, "get", return_value={"id": "app_123"}) as mock_get:
        application = certn_application_resource.get(resource_id="app_123")
        assert application["id"] == "app_123"
        mock_get.assert_called_once_with("app_123")


def test_update_application(certn_application_resource):
    with patch.object(
        certn_application_resource, "update", return_value={"id": "app_123", "status": "updated"}
    ) as mock_update:
        application = certn_application_resource.update(resource_id="app_123", data={"status": "updated"})
        assert application["status"] == "updated"
        mock_update.assert_called_once_with("app_123", {"status": "updated"})


def test_delete_application(certn_application_resource):
    with patch.object(
        certn_application_resource, "delete", return_value={"deleted": True, "id": "app_123"}
    ) as mock_delete:
        certn_application_resource.delete(resource_id="app_123")
        mock_delete.assert_called_once_with("app_123")


def test_list_applications_pagination(certn_application_resource):
    with patch.object(certn_application_resource, "list", return_value=[{"id": "app_123"}]) as mock_list:
        applications = certn_application_resource.list(page=1, size=10, starting_after="app_122")
        assert isinstance(applications, list)
        assert applications[0]["id"] == "app_123"
        mock_list.assert_called_once_with(page=1, size=10, starting_after="app_122")
