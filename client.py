
import paramiko
from fakefig import HOST, PORT, UNAME, UPWD, KEYPATH  # ,  LANDING
from decorators import handle_excepts, dispatch
# import os
# import logging

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

    @handle_excepts
    def connect(self):
        """
            Using paramiko utils, establish
            an sftp connection
        """
        # TODO @mfwolffe make grace or some such thing

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

    @handle_excepts
    def upload_thing(self, lPath):
        # TODO @mfwolffe write me lol
        return False

    def disconnect(self):
        """
            As it stands, gracefully close sftp
            session and ssh connection. I think
            I've got most of the possible races?
        """
        # DONE @mfwolffe write me lol
        # if not self.connected:
        #     print("No active connection")
        #     return

        if not self.client:
            dispatch(4, "No active connection.")

        if self.sftp:
            self.sftp.close()
            dispatch(4, "SFTP session closed.")

        if self.client:
            self.client.close()
            dispatch(4, "SSH connection closed.")

        dispatch(4, "Connection to host severed cleanly.")
