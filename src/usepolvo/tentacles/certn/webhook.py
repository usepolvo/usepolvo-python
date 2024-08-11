from usepolvo.arms.base_webhook import BaseWebhook


class CertnWebhook(BaseWebhook):
    def get_event_type(self, payload):
        return payload.get("event_type")

    async def default_handler(self, payload):
        """Default handler for unhandled Certn webhook events."""
        print(f"Received unhandled Certn webhook event: {payload.get('event_type')}")
        return {"status": "unhandled", "event_type": payload.get("event_type")}
