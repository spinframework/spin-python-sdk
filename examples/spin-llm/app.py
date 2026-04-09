from spin_sdk import http, llm
from spin_sdk.http import Request, Response

class HttpHandler(http.Handler):
    async def handle_request(self, request: Request) -> Response:
        res = llm.infer("all-minilm-l6-v2", "tell me a joke")
        print(res.text)
        print(res.usage)
        res = llm.infer_with_options("all-minilm-l6-v2", "what is the theory of relativity", llm.InferencingParams(temperature=0.5))
        print(res.text)
        print(res.usage)
        return Response(
            200,
            {"content-type": "text/plain"},
            bytes("Hello from Python!", "utf-8")
        )
