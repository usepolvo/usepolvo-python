import hmac
import hashlib


def verify_hmac_signature(payload, signature, secret_key):
    """Verify the webhook signature using HMAC."""
    computed_signature = hmac.new(secret_key.encode(), payload.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(computed_signature, signature):
        raise ValueError("Invalid webhook signature")
