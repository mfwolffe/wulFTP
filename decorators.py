# decorators for wulFTP routines

import socket
import logging
import paramiko


# TODO @mfwolffe jump table for log methods
#                maybe enum for readability
#

# NOTE: by default getlogger will create or retrieve a socalled
#       'named logger' which allows for referencing a logger across files
#       if the logger exists, it just retrieves it
logga = logging.getLogger("sftp_logger")

# NOTE: maybe counterintuitive but the logger
#       will not propagate anything itself does not
#       capture, so in order for both handlers (below)
#       to behave, logga's gotta capture minimum set accepted
#       by the handla's 
#
logga.setLevel(logging.INFO)

# logging to both console and a file I believe
# requires this approach of multiple handlers
# NOTE: console handler ignores INFO dispatches
#       file handler accepts everything 
#
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.WARNING)
console_handler.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))

file_handler = logging.FileHandler('sftp.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter("[%(asctime)s] [%(levelname)s] %(message)s")

logga.addHandler(file_handler)
logga.addHandler(console_handler)


LOG_LEVELS = {0: logging.CRITICAL, 1: logging.ERROR, 2: logging.WARNING, 3: logging.DEBUG, 4: logging.INFO}


def dispatch(level: int, msg: str, err=None):
    # conditions on none?
    out = f"{msg}: {err}" if err else msg
    logga.log(LOG_LEVELS[level], out)

# SEVERETIES = {0: "Fatal", 1: "Error", 2: "Warning", 3: "Internal", 4: "Info"}
# def dispatch(level: int, msg: str, err=None):
    # print(f"[{SEVERETIES[level]}] {msg}: {'' if err is None else err}")


def handle_excepts(fn):
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except paramiko.AuthenticationException as e:
            dispatch(0, "Authentication Failure. Check credentials", e)
        except paramiko.BadHostKeyException as e:
            dispatch(0, "Host key mismatch. Alert Matt", e)
        except paramiko.SSHException as e:
            dispatch(0, "SSH Error", e)
        except socket.timeout as e:
            dispatch(0, "Connection timeout. Server may be offline", e)
        except EOFError as e:
            dispatch(0, "Connection closed unexpectedly", e)
        except FileNotFoundError as e:
            if "upload" in fn.__name__:
                dispatch(0, "File not found", e)
            else:
                dispatch(3, "Configuration/log not found")
        except PermissionError as e:
            dispatch(2, "Permission denied", e)
        except Exception as e:
            dispatch(1, f"Unexpected error in {fn.__name__}", e)
        return False
    return wrapper
