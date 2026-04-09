from spin_sdk import http
from spin_sdk.http import Request, Response, send

class HttpHandler(http.Handler):
    async def handle_request(self, request: Request) -> Response:
        try:
            url = request.headers["url"]
        except KeyError:
            return Response(
                400,
                {"content-type": "text/plain"},
                bytes("Please specify `url` header", "utf-8")
            )

        resp = await send(Request("GET", url, {}, None))
        resp.headers = http.strip_forbidden_headers(resp.headers)
        return resp
