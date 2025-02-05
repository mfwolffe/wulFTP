
import paramiko
from decorators import handle_excepts, dispatch
from fakefig    import HOST, PORT, UNAME, UPWD, KEYPATH, LANDING, DFAULTKEY, VALIDKEYS
import os


class Client:
    def __init__(self):
        self.sftp       = None
        self.client     = None
        self.connected  = False

    def load_key(self, filepath, key_type=DFAULTKEY, passphrase=None):
        """
            Use paramiko util to load arbitrary type private key
        """
        if not os.path.exists(filepath):
            raise ValueError(f"Key file not found: {filepath}")

        if key_type not in VALIDKEYS:
            raise ValueError(f"Unsupported key type: {key_type}")

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

        self.client = paramiko.SSHClient()
        # TODO @mfwolffe off races the to
        #                probably just lock it
        #                consider making atomic in interim?
        self.sftp = None

        if KEYPATH:
            try:
                pkey = self.load_key(KEYPATH, key_type="Ed25519")
            except ValueError as e:
                dispatch(2, "Key error. Retrying with RSA...", e)
                try:
                    pkey = self.load_key(KEYPATH, key_type="RSA")
                except ValueError as e:
                    dispatch(0, "Unable to proceed with connection", e)
                    return False
            self.client.connect(HOST, PORT, UNAME, pkey=pkey)
        else:
            self.client.connect(HOST, PORT, UNAME, UPWD)

        print(f"Successfully connected to {HOST}")
        return True

    @handle_excepts
    def upload_thing(self, lPath):
        # DONE? @mfwolffe write me lol
        #                 done does not exist

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
            dispatch(0, f"Filepath '{fName}' not found.")
            return False

        try:
            # TODO @mfwolffe write (think
            #                about) upload routine
            pass
        except PermissionError as e:
            dispatch(2, "Permission denied", e)
            return False

        # default to failure
        dispatch(0, f"Upload of '{fName}' not completed.")
        return False

    @handle_excepts
    def disconnect(self):
        """
            As it stands, gracefully close sftp
            session and ssh connection. I think
            I've got most of the possible races?
            (caught by decorator)
        """

        if not self.client:
            dispatch(4, "No active connection.")
            return False

        if self.sftp:
            self.sftp.close()
            dispatch(4, "SFTP session closed.")

        if self.client:
            self.client.close()
            dispatch(4, "SSH connection closed.")

        dispatch(4, "Connection to host severed cleanly.")

        return True
