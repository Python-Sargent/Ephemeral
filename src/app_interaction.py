# Discord RPC

try:
    import discordrpc

    secret = 1353773230820691989
    class DiscordRPC:
        rpc = discordrpc.RPC(app_id = secret)
        def set(self, dtl, st):
            self.rpc.set_activity(state=st, details=dtl)
        def stop(self):
            self.rpc.disconnect()
        def run(self):
            self.rpc.run()
except:
    class DiscordRPC:
        def set(_, __, ___):
            pass
        def stop(_):
            pass
        def run(_):
            pass