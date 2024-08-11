from abc import ABC, abstractmethod
from usepolvo.ink.validators import verify_hmac_signature


class BaseWebhook(ABC):
    def __init__(self):
        self.handlers = {}
        self.secret_key = None

    def set_secret_key(self, key):
        self.secret_key = key

    def register(self, event_type, handler=None):
        if handler is None:
            return lambda h: self.register(event_type, h)
        self.handlers[event_type] = handler

    async def process(self, payload, signature=None):
        if self.secret_key and signature:
            self.verify_signature(payload, signature)

        event_type = self.get_event_type(payload)
        handler = self.handlers.get(event_type, self.default_handler)
        return await handler(payload)

    def verify_signature(self, payload, signature):
        verify_hmac_signature(payload, signature, self.secret_key)

    @abstractmethod
    def get_event_type(self, payload):
        """Extract the event type from the payload."""
        pass

    @abstractmethod
    async def default_handler(self, payload):
        """Default handler for unhandled webhook events."""
        pass
