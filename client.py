
import paramiko
from fakefig import HOST, PORT, UNAME, UPWD, KEYPATH, LANDING, DFAULTKEY, VALIDKEYS
from decorators import handle_excepts, dispatch
import os
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

    def load_key(filepath, key_type=DFAULTKEY, passphrase=None):
        # TODO @mfwolffe think about the decorator and the current
        #                current exception handling
        """
            Use paramiko util to load arbitrary type private key
        """
        if not os.path.exists(filepath):
            raise ValueError(f"Key file not found: {filepath}")

        if key_type not in VALIDKEYS:
            raise ValueError("Unsupported key type: {key_type}")

        try:
            key = VALIDKEYS[key_type].from_private_key_file(filepath, password=passphrase)

            if key_type == "RSA" and key.bits < 2048:
                raise ValueError("RSA key too weak.")

            return key
        except paramiko.PasswordRequiredException:
            raise ValueError(f"The {key_type} key at {filepath} requires passphrase")
        except paramiko.SSHException as e:
            raise ValueError(f"Failed to load {key_type} from {filepath}: {e}")
        except IOError as e:
            raise ValueError(f"Unable to open file {filepath}: {e}")

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

            # TODO @mfwolffe either enforce an algo or allow choice
            #                between strong types
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
        # DONE? @mfwolffe write me lol

        if not self.sftp:
            dispatch(0, "No active SFTP session. Unable to upload file.")
            return False

        # extract filename from local path
        # and construct destination path
        # NOTE: these are simple string operations and will not
        # throw for nonexistant file
        fName       = os.path.basename(lPath)
        remote_path = os.path.join(LANDING, fName)  # noqa: F841

        if not os.path.exists(lPath):
            dispatch(0, "Filepath '{fname}' not found.")
            return False

        try:
            # write uploader
            pass
        except PermissionError as e:
            dispatch(2, "Permission denied", e)
            return False

        # default to failure
        dispatch(2, "Upload of '{fName}' not completed.")
        return False

    @handle_excepts
    def disconnect(self):
        """
            As it stands, gracefully close sftp
            session and ssh connection. I think
            I've got most of the possible races?
            (caught by decorator)
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
