import paramiko
import os
from fakefig import HOST, PORT, UNAME, UPWD, KEYPATH, LANDING


class Client:
    def __init__(self):
        self.client = None
        self.sftp = None

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
        # TODO @mfwolffe write me lol
        pass
            
