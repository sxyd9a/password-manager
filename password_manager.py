import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class PasswordManager:
    def __init__(self):
        self.salt_file = "salt.salt"
        self.data_file = "passwords.txt"
        self.fernet = self._load_fernet()

    def _load_fernet(self):
        master_pwd = input("Enter master password: ").encode()

        #Generate salt if it doesn't exist
        if not os.path.exists(self.salt_file):
            with open(self.salt_file, "wb") as f:
                f.write(os.urandom(16))

        with open(self.salt_file, "rb") as f:
            salt = f.read()

        #Derive key using PBKDF2
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100_000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(master_pwd))
        return Fernet(key)

    def add_password(self):
        name = input("Account name: ")
        pwd = input("Password: ")

        if "|" in pwd:
            print("Error: Password cannot contain the '|' character.")
            return

        encrypted = self.fernet.encrypt(pwd.encode()).decode()
        try:
            with open(self.data_file, 'a') as f:
                f.write(f"{name}|{encrypted}\n")
            print("Password added.")
        except Exception as e:
            print("Failed to write password:", e)

    def view_passwords(self):
        try:
            with open(self.data_file, 'r') as f:
                for line in f.readlines():
                    line = line.strip()
                    if not line:
                        continue
                    user, encrypted = line.split("|")
                    decrypted = self.fernet.decrypt(encrypted.encode()).decode()
                    print(f"User: {user} | Password: {decrypted}")
        except FileNotFoundError:
            print("No passwords stored yet.")
        except Exception as e:
            print("Error reading passwords:", e)

    def run(self):
        while True:
            mode = input("Would you like to add a new password or view existing ones (view, add), press q to quit? ").lower()
            if mode == "q":
                break
            elif mode == "view":
                self.view_passwords()
            elif mode == "add":
                self.add_password()
            else:
                print("Invalid mode.")

if __name__ == "__main__":
    manager = PasswordManager()
    manager.run()