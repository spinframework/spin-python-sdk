from spin_sdk.wit import exports

class RedisHandler(exports.RedisHandler):
    async def handle_message(self, message: bytes) -> None:
        print(message)
