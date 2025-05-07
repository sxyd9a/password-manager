from cryptography.fernet import Fernet
import os

class MasterPassword:
    def __init__(self, key_file='key.key'):
        self.key_file = key_file
        self.key = None

    def write_key(self):
        key = Fernet.generate_key()
        with open(self.key_file, "wb") as f:
            f.write(key)

    def load_key(self):
        with open(self.key_file, "rb") as f:
            return f.read()

    def setup_or_verify(self):
        if not os.path.exists(self.key_file):
            print("No master password set. Creating new key...")
            self.write_key()

        self.key = self.load_key()
        user_input = input("Enter master password: ").strip()

        if user_input.lower() != "taipan":
            print("Incorrect master password. Exiting.")
            exit()