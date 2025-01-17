from typing import Any, Dict

from usepolvo.arms.base_webhook import BaseWebhook
from usepolvo.tentacles.linear.webhooks.schemas import LinearWebhookPayload


class LinearWebhook(BaseWebhook):
    def __init__(self):
        super().__init__()
        # ref: https://docs.certn.co/api/v/certn-api-v-1.0/guides/use-the-api/webhooks#signature-verification
        self.signature_header = "Linear-Signature"

        # Register handlers
        self.register("request_enhanced_identity_verification", self.handle_enhanced_identity_verification)
        # Add more handlers for other event types as needed

    def get_event_type(self, payload: Dict[str, Any]) -> str:
        return LinearWebhookPayload.from_dict(payload).get_event_type()

    async def process(self, payload: Dict[str, Any], signature: str = None) -> Any:
        if self.secret_key and signature:
            self.verify_signature(payload, signature)

        validated_payload = LinearWebhookPayload.from_dict(payload)
        event_type = validated_payload.get_event_type()
        handler = self.handlers.get(event_type, self.default_handler)
        return await handler(validated_payload)

    async def default_handler(self, payload: LinearWebhookPayload):
        print(f"Unhandled event: {payload.get_event_type()}")
        print(f"Payload: {payload.model_dump()}")

    async def handle_enhanced_identity_verification(self, payload: LinearWebhookPayload):
        print(f"Enhanced identity verification requested")
        print(f"Created: {payload.created}, Submitted: {payload.submitted_time}")
        # Add more processing as needed

    # Add more specific handlers for other event types as needed
