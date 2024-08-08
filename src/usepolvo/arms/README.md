# Arms

The `arms` directory contains shared functionality and base classes used across different API integrations in usepolvo-python.

## Contents

- `base_client.py`: Abstract base class for API clients.
- `base_resource.py`: Abstract base class for API resources.
- `auth.py`: Authentication utilities and base classes.
- `pagination.py`: Common pagination handling utilities.

## Usage

When implementing a new API integration, inherit from the base classes provided here. For example:

```python
from usepolvo.arms.base_client import BaseClient

class MyServiceClient(BaseClient):
    # Implement service-specific methods here
    ...
```

## Guidelines

- Keep the code in this directory generic and applicable to multiple API integrations.
- Document any changes to base classes, as they may affect multiple integrations.
- When adding new shared functionality, consider its potential impact on existing integrations.

## Testing

Unit tests for the arms module can be found in `tests/arms/`. Ensure all base functionality is well-tested.
