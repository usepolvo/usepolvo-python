from aiohttp import web
from pyngrok import ngrok


class WebhookServer:
    def __init__(self, webhook_handler, path, port=8080):
        self.webhook_handler = webhook_handler
        self.path = path
        self.port = port
        self.app = web.Application()
        self.app.router.add_post(path, self._handle_webhook)

    async def _handle_webhook(self, request):
        payload = await request.json()
        signature = request.headers.get(self.webhook_handler.signature_header)
        try:
            await self.webhook_handler.process(payload, signature)
            return web.Response(status=200, text="Webhook processed successfully")
        except ValueError as e:
            return web.Response(status=400, text=str(e))

    async def start(self):
        runner = web.AppRunner(self.app)
        await runner.setup()
        site = web.TCPSite(runner, "localhost", self.port)
        await site.start()

        ngrok_tunnel = ngrok.connect(self.port)
        print(f"Ngrok tunnel established: {ngrok_tunnel.public_url}")
        print(f"Webhook URL: {ngrok_tunnel.public_url}{self.path}")
        print(f"Use this URL in your webhook settings")

        return ngrok_tunnel
