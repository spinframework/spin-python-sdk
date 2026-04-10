from spin_sdk import http
from spin_sdk.http import Request, Response
from spin_sdk.sqlite import Connection, Value_Text, Value_Integer
from spin_sdk.util import collect

class HttpHandler(http.Handler):
    async def handle_request(self, request: Request) -> Response:
        with await Connection.open_default() as db:
            _, stream, result = await db.execute(
                "CREATE TABLE IF NOT EXISTS example (id INTEGER NOT NULL PRIMARY KEY, value TEXT NOT NULL)",
                []
            )
            await collect((stream, result))

            insert = "INSERT INTO example (id, value) VALUES (?, ?) ON CONFLICT (id) DO UPDATE SET value=excluded.value"

            _, stream, result = await db.execute(insert, [Value_Integer(1), Value_Text("foo")])
            await collect((stream, result))
            
            _, stream, result = await db.execute(insert, [Value_Integer(2), Value_Text("bar")])
            await collect((stream, result))
            
            columns, stream, result = await db.execute("SELECT * FROM example WHERE id > (?);", [Value_Integer(0)])
            rows = await collect((stream, result))

            assert columns == ["id", "value"]
            assert len(rows) == 1
            assert isinstance(rows[0].values[0], Value_Integer)
            assert rows[0].values[0].value == 2
            assert isinstance(rows[0].values[1], Value_Text)
            assert rows[0].values[1].value == "bar"

        return Response(
            200,
            {"content-type": "text/plain"},
            bytes(str(rows), "utf-8")
        )
