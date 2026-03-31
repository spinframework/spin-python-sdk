from spin_sdk import http, postgres
from spin_sdk.http import Request, Response


def format_value(db_value) -> str:
    if hasattr(db_value, "value"):
        return str(db_value.value)
    return "NULL"


def format_rowset(rowset) -> str:
    lines = []
    col_names = [col.name for col in rowset.columns]
    lines.append(" | ".join(col_names))
    lines.append("-" * len(lines[0]))
    for row in rowset.rows:
        values = [format_value(v) for v in row]
        lines.append(" | ".join(values))
    return "\n".join(lines)


class WasiHttpIncomingHandler020(http.IncomingHandler):
    def handle_request(self, request: Request) -> Response:
        with postgres.open("user=postgres dbname=spin_dev host=127.0.0.1") as db:
            rowset = db.query("SELECT * FROM test", [])
            result = format_rowset(rowset)

        return Response(200, {"content-type": "text/plain"}, bytes(result, "utf-8"))
