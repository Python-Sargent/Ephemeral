# python
#
# Multiplayer Networking Game
# 

from os import linesep
import datetime

verbose = True

def _loglvl(message: str, level: str):
    return "[" + level + "] " + message

def _logmsg(message, filename):
    try:
        with open(filename, "a") as log_file:  # "a" for append mode
            log_file.write(message + linesep) #os.linesep adds the correct line ending for the OS.
            log_file.close()
    except OSError as e:
        print(f"Error writing to file {filename}: {e}")

def log(message, loglevel = "Info"):
    logmsg = _loglvl(str(message), str(loglevel))
    now = datetime.datetime.now()
    msg = str(now.strftime("%Y-%m-%d %H:%M:%S")) + ": " + logmsg
    if loglevel == "Info":
        if verbose is True: print(msg, end="\n")
    else:
        print(msg, end="\n")
    _logmsg(msg, "log.txt")

def log_begin():
    mode = ""
    if verbose is True: mode = "Verbose"
    else: mode = "Warn"
    log("Logging started with mode " + mode + """
 ________  _______   __    __  ________  __       __  ________  _______    ______   __       
/        |/       \\ /  |  /  |/        |/  \\     /  |/        |/       \\  /      \\ /  |      
$$$$$$$$/ $$$$$$$  |$$ |  $$ |$$$$$$$$/ $$  \\   /$$ |$$$$$$$$/ $$$$$$$  |/$$$$$$  |$$ |      
$$ |__    $$ |__$$ |$$ |__$$ |$$ |__    $$$  \\ /$$$ |$$ |__    $$ |__$$ |$$ |__$$ |$$ |      
$$    |   $$    $$/ $$    $$ |$$    |   $$$$  /$$$$ |$$    |   $$    $$< $$    $$ |$$ |      
$$$$$/    $$$$$$$/  $$$$$$$$ |$$$$$/    $$ $$ $$/$$ |$$$$$/    $$$$$$$  |$$$$$$$$ |$$ |      
$$ |_____ $$ |      $$ |  $$ |$$ |_____ $$ |$$$/ $$ |$$ |_____ $$ |  $$ |$$ |  $$ |$$ |_____ 
$$       |$$ |      $$ |  $$ |$$       |$$ | $/  $$ |$$       |$$ |  $$ |$$ |  $$ |$$       |
$$$$$$$$/ $$/       $$/   $$/ $$$$$$$$/ $$/      $$/ $$$$$$$$/ $$/   $$/ $$/   $$/ $$$$$$$$/ 
""")

def log_end():
    log("Logging Finished\n\n")