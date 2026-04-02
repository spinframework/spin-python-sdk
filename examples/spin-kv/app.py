from spin_sdk import http, key_value
from spin_sdk.http import Request, Response
from spin_sdk.key_value import Store

class WasiHttpHandler030Rc20260315(http.Handler):
    async def handle_request(self, request: Request) -> Response:
        with await key_value.open_default() as a:
            await a.set("test", bytes("hello world!", "utf-8"))
            print(await get_keys(a))
            print(await a.exists("test"))
            print(await a.get("test"))
            print(await a.delete("test"))
            print(await get_keys(a))
            
        return Response(
            200,
            {"content-type": "text/plain"},
            bytes("Hello from Python!", "utf-8")
        )

async def get_keys(Store) -> list[str]:
    stream, future = await Store.get_keys()
    keys = []

    while True:
        batch = await stream.read(max_count=100)
        if not batch:
            break
        keys.extend(batch)

    return keys