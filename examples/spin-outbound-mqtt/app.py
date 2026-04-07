from spin_sdk import http, mqtt 
from spin_sdk.mqtt import Qos
from spin_sdk.http import Request, Response

class WasiHttpHandler030Rc20260315(http.Handler):
    async def handle_request(self, request: Request) -> Response:
        with await mqtt.open("mqtt://localhost:1883?client_id=client001", "user", "password", 30) as conn:
            await conn.publish("telemetry", bytes("Eureka!", "utf-8"), Qos.AT_LEAST_ONCE)

        return Response(
            200,
            {"content-type": "text/plain"},
            bytes("Sent outbound mqtt message!", "utf-8")
        )
