from master_password import MasterPassword
from password_manager import PasswordManager

def main():
    #Verify master password
    master = MasterPassword()
    master.setup_or_verify()

    #Initialize password manager
    pm = PasswordManager()

    while True:
        mode = input("Would you like to add a new password or view existing ones (view, add), press q to quit? ").lower()
        if mode == "q":
            break
        elif mode == "view":
            pm.view_passwords()
        elif mode == "add":
            pm.add_password()
        else:
            print("Invalid mode.")

if __name__ == "__main__":
    main()