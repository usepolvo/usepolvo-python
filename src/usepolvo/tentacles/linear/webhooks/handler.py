from typing import Any, Dict, Optional

from usepolvo.arms.base_webhook import BaseWebhook
from usepolvo.tentacles.linear.config import get_settings
from usepolvo.tentacles.linear.webhooks.schemas import LinearWebhookPayload


class LinearWebhook(BaseWebhook):
    def __init__(self, webhook_secret: Optional[str] = None):
        super().__init__()
        self.signature_header = "Linear-Signature"

        # Initialize settings
        self.settings = get_settings()

        # Set webhook secret from argument or fall back to settings
        secret = webhook_secret if webhook_secret else self.settings.LINEAR_WEBHOOK_SECRET
        if secret:
            self.set_secret_key(secret)

    def get_event_type(self, payload: Dict[str, Any]) -> str:
        return LinearWebhookPayload(**payload).get_event_type()

    async def process(self, payload: Dict[str, Any]) -> Any:
        try:
            validated_payload = LinearWebhookPayload(**payload)
        except Exception as e:
            print(f"Invalid payload: {e}")
            raise
        event_type = validated_payload.get_event_type()
        handler = self.handlers.get(event_type, self.default_handler)
        return await handler(validated_payload)

    async def default_handler(self, payload: LinearWebhookPayload):
        """Default handler for unhandled webhook events"""
        event_type = payload.get_event_type()
        print(f"Unhandled event: {event_type}")
        return {"status": "ok"}
