# decorators for wulFTP routines

# import paramiko
# import socket

def handle_excepts(fn):
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            print(f"Fatal: Unexpected Error: {e}")
        return False
    return wrapper
