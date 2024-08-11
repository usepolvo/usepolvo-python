import asyncio
from abc import ABC, abstractmethod

from aiohttp import web
from pyngrok import ngrok

from usepolvo.ink.validators import verify_hmac_signature


class BaseWebhook(ABC):
    def __init__(self):
        self.handlers = {}
        self.secret_key = None
        self.signature_header = None
        self._server = None
        self._ngrok_tunnel = None

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

    async def _handle_webhook(self, request):
        payload = await request.json()
        signature = request.headers.get(self.signature_header)
        try:
            await self.process(payload, signature)
            return web.Response(status=200, text="Webhook processed successfully")
        except ValueError as e:
            return web.Response(status=400, text=str(e))

    async def start_server(self, path, port=8080):
        app = web.Application()
        app.router.add_post(path, self._handle_webhook)

        runner = web.AppRunner(app)
        await runner.setup()
        self._server = web.TCPSite(runner, "localhost", port)
        await self._server.start()

        self._ngrok_tunnel = ngrok.connect(port)
        print(f"Ngrok tunnel established: {self._ngrok_tunnel.public_url}")
        print(f"Webhook URL: {self._ngrok_tunnel.public_url}{path}")
        print(f"Use this URL in your webhook settings")

    async def stop_server(self):
        if self._server:
            await self._server.stop()

        if self._ngrok_tunnel:
            try:
                ngrok.disconnect(self._ngrok_tunnel.public_url)
            except Exception as e:
                print(f"Failed to disconnect ngrok tunnel: {e}")

        # Ensure ngrok process is terminated
        try:
            ngrok.kill()
        except Exception as e:
            print(f"Failed to kill ngrok process: {e}")

    async def run(self, path, port=8080):
        await self.start_server(path, port)
        try:
            # Keep the server running
            while True:
                await asyncio.sleep(1)
        except asyncio.CancelledError:
            # Handle cancellation gracefully
            print("Received cancellation, shutting down...")
        finally:
            await self.stop_server()
