from spin_sdk import http, key_value, util
from spin_sdk.http import Request, Response
from spin_sdk.key_value import Store

class HttpHandler(http.Handler):
    async def handle_request(self, request: Request) -> Response:
        with await key_value.open_default() as a:
            await a.set("test", bytes("hello world!", "utf-8"))
            print(await util.collect(await a.get_keys()))
            print(await a.exists("test"))
            print(await a.get("test"))
            await a.delete("test")
            print(await util.collect(await a.get_keys()))
            
        return Response(
            200,
            {"content-type": "text/plain"},
            bytes("Hello from Python!", "utf-8")
        )
