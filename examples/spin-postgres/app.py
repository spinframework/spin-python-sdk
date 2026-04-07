from spin_sdk import http, postgres
from spin_sdk.http import Request, Response
from spin_sdk.postgres import RowSet, DbValue


def format_value(db_value: DbValue) -> str:
    if hasattr(db_value, "value"):
        return str(db_value.value)
    return "NULL"


def format_rowset(rowset: RowSet) -> str:
    lines = []
    col_names = [col.name for col in rowset.columns]
    lines.append(" | ".join(col_names))
    lines.append("-" * len(lines[0]))
    for row in rowset.rows:
        values = [format_value(v) for v in row]
        lines.append(" | ".join(values))
    return "\n".join(lines)


class WasiHttpHandler030Rc20260315(http.Handler):
    async def handle_request(self, request: Request) -> Response:
        with await postgres.open("user=postgres dbname=spin_dev host=localhost sslmode=disable password=password") as db:
            rowset = db.query("SELECT * FROM test", [])
            result = format_rowset(rowset)

        return Response(200, {"content-type": "text/plain"}, bytes(result, "utf-8"))
