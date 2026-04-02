from spin_sdk.wit import exports

class SpinRedisInboundRedis300(exports.SpinRedisInboundRedis300):
    async def handle_message(self, message: bytes):
        print(message)
