# decorators for wulFTP routines

import socket
import paramiko
from   log_utils import dispatch  # noqa: E271
                                # ^ why am i like this (it's not funny) &-> # noqa: E116


def handle_excepts(context="generic"):
    def decorator(fn):
        def wrapper(*args, **kwargs):
            try:
                return fn(*args, **kwargs)
            except paramiko.AuthenticationException as e: dispatch(0, "Authentication Failure. Check credentials", e)
            except paramiko.BadHostKeyException as e:     dispatch(0, "Host key mismatch. Alert Matt", e)
            except paramiko.SSHException as e:            dispatch(0, "SSH Error", e)
            except socket.timeout as e:                   dispatch(0, "Connection timeout. Server may be offline", e)
            except EOFError as e:                         dispatch(0, "Connection closed unexpectedly", e)
            except FileNotFoundError as e:
                if context == "upload":
                    dispatch(0, "File not found", e)
                else:
                    dispatch(3, "Configuration/log not found")
            except PermissionError as e:                  dispatch(2, "Permission denied", e)
            except Exception as e:                        dispatch(1, f"Unexpected error in {fn.__name__}", e)
            return False
        return wrapper
