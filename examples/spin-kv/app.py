from typing import TypeVar, Tuple, List
from componentize_py_types import Result, Err
from componentize_py_async_support.streams import StreamReader
from componentize_py_async_support.futures import FutureReader
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
            await a.delete("test")
            print(await get_keys(a))
            
        return Response(
            200,
            {"content-type": "text/plain"},
            bytes("Hello from Python!", "utf-8")
        )

async def get_keys(store: Store) -> list[str]:
    stream, future = await store.get_keys()
    with stream, future:
        keys = []
        while not stream.writer_dropped:
            keys += await stream.read(max_count=100)
        return keys
