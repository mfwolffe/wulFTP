import paramiko
import os
from fakefig import HOST, PORT, UNAME, UPWD, KEYPATH, LANDING
# TODO @mfwolffe log instead of print calls
import logging

# TODO @mfwolffe
#       - threading for uploads
#       - logging to logfile instead of console
#       - more robust connect from a sec standpoint
#       - handling for bad keys/pass, etc


class Client:
    def __init__(self):
        self.sftp       = None
        self.client     = None
        self.connected  = False

    def connect(self):
        """
            Using paramiko utils, establish 
            an sftp connection
        """

        try:
            self.client = paramiko.SSHClient()

            # TODO @mfwolffe do not automatically add to known hosts file
            #                man in the middle...                
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            if KEYPATH:
                pkey = paramiko.RSAKey(filename=KEYPATH)
                self.client.connect(HOST, PORT, UNAME, pkey=pkey)
            else:
                self.client.connect(HOST, PORT, UNAME, UPWD)

            self.sftp = self.client.open_sftp()
            print(f"Connected to {HOST}")
            return True
        except Exception as e:
            print(f"ERROR: Failed to connect to {HOST}.\nMESSAGE: {e}")
            return False

    def upload_thing(self, lPath):
        # TODO @mfwolffe write me lol
        return False

    def disconnect(self):
        # DONE @mfwolffe write me lol
        # if not self.connected:
        #     print("No active connection")
        #     return

        try:
            if self.sftp:
                try:
                    self.sftp.close()
                    print("Notice: SFTP session closed.")
                except paramiko.sftp.SFTPError as e:
                    print(f"Warning: Failed to close SFTP session: {e}")
                except Exception as e:
                    print(f"Fatal: Unexpected error closing SFTP session: {e}")

            if self.client:
                try:
                    self.client.close()
                    print("Notice: SSH connection closed.")
                except paramiko.SSHException as e:
                    print(f"Warning: Failed to close SSH connection: {e}")
                except EOFError:
                    print("Warning: SSH connection already closed by host")
                except Exception as e:
                    print(f"Fatal: Unexpected error closing SSH connection: {e}")
                    
        except Exception as e:
            print(f"Fatal: Unexpected error during disconnect subroutine: {e}")            
