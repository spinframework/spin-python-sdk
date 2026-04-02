from spin_sdk.http import Handler, Request, Response

class WasiHttpHandler030Rc20260315(Handler):
    async def handle_request(self, request: Request) -> Response:
        return Response(
            200,
            {"content-type": "text/plain"},
            bytes("Hello from Python!", "utf-8")
        )
