# Ink

The `ink` directory contains utility functions and helpers used throughout the usepolvo-python project.

## Contents

- `transformations.py`: Data transformation and conversion utilities.
- `validation.py`: Input validation helpers.
- `date_utils.py`: Date and time manipulation functions.
- `encryption.py`: Encryption and decryption utilities.

## Usage

Import and use these utilities in your integration code as needed. For example:

```python
from usepolvo.ink.transformations import camel_to_snake
from usepolvo.ink.validation import validate_email

# Use in your code
transformed_key = camel_to_snake("myCamelCaseString")
is_valid = validate_email("user@example.com")
```

## Adding New Utilities

When adding new utility functions:

1. Place them in an appropriate existing file or create a new file if needed.
2. Ensure the function is well-documented with docstrings.
3. Add corresponding unit tests in the `tests/ink/` directory.
4. Update this README if adding a new file or significant functionality.

## Guidelines

- Keep utility functions pure and side-effect free when possible.
- Prioritize reusability and generality in this module.
- Use type hints to improve code clarity and enable static type checking.

## Testing

Comprehensive unit tests for all utility functions should be maintained in the `tests/ink/` directory.
