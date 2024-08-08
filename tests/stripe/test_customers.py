from unittest.mock import patch


def test_create_customer(stripe_customer_resource):
    with patch.object(
        stripe_customer_resource.stripe.Customer, "create", return_value={"email": "test@example.com"}
    ) as mock_create:
        customer = stripe_customer_resource.create(data={"email": "test@example.com"})
        assert customer["email"] == "test@example.com"
        mock_create.assert_called_once_with(email="test@example.com")


def test_list_customers(stripe_customer_resource):
    with patch.object(stripe_customer_resource.stripe.Customer, "list", return_value=[{"id": "cus_123"}]) as mock_list:
        customers = stripe_customer_resource.list(page=1, size=10)
        assert isinstance(customers, list)
        assert customers[0]["id"] == "cus_123"
        mock_list.assert_called_once()


def test_get_customer(stripe_customer_resource):
    with patch.object(
        stripe_customer_resource.stripe.Customer, "retrieve", return_value={"id": "cus_123"}
    ) as mock_retrieve:
        customer = stripe_customer_resource.get(resource_id="cus_123")
        assert customer["id"] == "cus_123"
        mock_retrieve.assert_called_once_with("cus_123")


def test_update_customer(stripe_customer_resource):
    with patch.object(
        stripe_customer_resource.stripe.Customer,
        "modify",
        return_value={"id": "cus_123", "email": "updated@example.com"},
    ) as mock_modify:
        customer = stripe_customer_resource.update(resource_id="cus_123", data={"email": "updated@example.com"})
        assert customer["email"] == "updated@example.com"
        mock_modify.assert_called_once_with("cus_123", email="updated@example.com")


def test_delete_customer(stripe_customer_resource):
    with patch.object(
        stripe_customer_resource.stripe.Customer, "delete", return_value={"deleted": True, "id": "cus_123"}
    ) as mock_delete:
        stripe_customer_resource.delete(resource_id="cus_123")
        mock_delete.assert_called_once_with("cus_123")


def test_list_customers_pagination(stripe_customer_resource):
    with patch.object(stripe_customer_resource.stripe.Customer, "list", return_value=[{"id": "cus_123"}]) as mock_list:
        customers = stripe_customer_resource.list(page=1, size=10, starting_after="cus_122")
        assert isinstance(customers, list)
        assert customers[0]["id"] == "cus_123"
        mock_list.assert_called_once_with(limit=10, starting_after="cus_122")
