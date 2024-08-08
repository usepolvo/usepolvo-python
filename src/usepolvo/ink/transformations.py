from datetime import datetime


def transform_customer_data(data):
    """
    Transform customer data to match Stripe API format.
    """
    transformed = data.copy()
    if "created_at" in transformed:
        transformed["created"] = int(datetime.timestamp(transformed["created_at"]))
        del transformed["created_at"]
    return transformed


def transform_response_data(data):
    """
    Transform response data from Stripe API to match internal format.
    """
    transformed = data.copy()
    if "created" in transformed:
        transformed["created_at"] = datetime.fromtimestamp(transformed["created"])
        del transformed["created"]
    return transformed


def snake_to_camel(snake_str: str) -> str:
    """
    Convert a snake_case string to camelCase.

    :param snake_str: The input string in snake_case
    :return: The string converted to camelCase
    """
    components = snake_str.split("_")
    return components[0] + "".join(x.title() for x in components[1:])
