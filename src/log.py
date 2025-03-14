# python
#
# Multiplayer Networking Game
# 

import datetime

def _loglvl(message: str, level: str):
    return "[" + level + "] " + message

def log(message, loglevel = "Info"):
    logmsg = _loglvl(str(message), str(loglevel))
    now = datetime.datetime.now()
    print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + ": " + logmsg, end="\n")