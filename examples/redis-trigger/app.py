from spin_sdk.wit import exports

class FermyonSpinInboundRedis(exports.FermyonSpinInboundRedis):
    def handle_message(self, message: bytes):
        print(message)
