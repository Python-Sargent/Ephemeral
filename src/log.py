# python 3.13
#
# Ephemeral Logging
# 

from os import linesep
import datetime

verbose = True

class LogLevel:
    Info = "Info"
    Warn = "Warn"
    Error = "Error"

def __loglvl__(message: str, level: str):
    return "[" + level + "] " + message

def __logmsg__(message: str, filename: str):
    try:
        with open(filename, "a") as log_file:  # "a" for append mode
            log_file.write(message + linesep) #os.linesep adds the correct line ending for the OS.
    except OSError as e:
        print(f"Error writing to file {filename}: {e}")

def __create_message__(message: str, loglevel: str):
    logmsg = __loglvl__(str(message), str(loglevel))
    now = datetime.datetime.now()
    msg = str(now.strftime("%Y-%m-%d %H:%M:%S")) + ": " + logmsg
    if loglevel == LogLevel.Info:
        if verbose is True: print(msg, end="\n")
    else:
        print(msg, end="\n")
    return msg

def log(message, loglevel = "Info"):
    __logmsg__(__create_message__(message, loglevel), "log.txt")

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

class Log:
    def __init__(self, filename):
        self.filename = filename
    def log(self, message, loglevel="Info"):
        __logmsg__(__create_message__(message, loglevel), self.filename)