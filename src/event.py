# python 3.13
#
# Ephemeral Event Definition
# 

import threading

GlobalEvents = {}

class EventThread(threading.Thread):
    def __init__(self, event, action, args):
        super().__init__(None, action, "CLIENT_THREAD", args, {})
        self.daemon = True
        self.event = event

class Event:
    def __init__(self, action, id, do_thread=False) -> None:
        self.action = action
        self.id = id
        self.do_thread = do_thread
    def trigger(self, args):
        try:
            if self.do_thread:
                ethread = EventThread(self, self.action, args)
                ethread.start()
            else:
                self.action(args)
        except IndexError:
            raise ValueError(f"Event {self.id} >> Inappropiate arguments: " + str(args))

def CreateGlobalEvent(action, id=len(GlobalEvents), do_thread=False):
    e = Event(action, id, do_thread)
    GlobalEvents[id] = e