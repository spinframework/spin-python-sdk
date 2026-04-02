from spin_sdk import http   
from spin_sdk.http import Request, Response, send

class WasiHttpHandler030Rc20260315(http.Handler):
    async def handle_request(self, request: Request) -> Response:
        try:
            url = request.headers["url"]
        except KeyError:
            return Response(
                400,
                {"content-type": "text/plain"},
                bytes("Please specify `url` header", "utf-8")
            )

        return await send(Request("GET", url, {}, None))
