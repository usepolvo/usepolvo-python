from usepolvo.arms.base_webhook import BaseWebhook


class StripeWebhook(BaseWebhook):
    def get_event_type(self, payload):
        return payload.get("type")

    async def default_handler(self, payload):
        """Default handler for unhandled Stripe webhook events."""
        print(f"Received unhandled Stripe webhook event: {payload.get('type')}")
        return {"status": "unhandled", "event_type": payload.get("type")}
