"""
Password Manager
----------------
A command-line password manager that securyptography.fernetrely stores and retrieves
passwords for different accounts using encryption.

How it works:
- A master password is used to derive an encryption key (PBKDF2).
- Account passwords are encrypted with Fernet (symmetric encryption)
  before being stored in a SQLite database.
- Passwords are only decrypted when you choose to view them.

Run:
    pip install cryptography
    python password_manager.py
"""

import sqlite3
import os
import base64
import getpass
import secrets
import string
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

DB_NAME = "passwords.db"
SALT_FILE = "salt.bin"


# ---------- Setup / encryption key handling ----------
def get_or_create_salt():
    if os.path.exists(SALT_FILE):
        with open(SALT_FILE, "rb") as f:
            return f.read()
    salt = os.urandom(16)
    with open(SALT_FILE, "wb") as f:
        f.write(salt)
    return salt


def derive_key(master_password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=200_000,
    )
    key = kdf.derive(master_password.encode())
    return base64.urlsafe_b64encode(key)


# ---------- Database setup ----------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service TEXT NOT NULL,
            username TEXT NOT NULL,
            encrypted_password BLOB NOT NULL
        )
    """)
    conn.commit()
    conn.close()


# ---------- Core operations ----------
def add_account(fernet):
    service = input("Service/Website name: ").strip()
    username = input("Username/Email: ").strip()

    choice = input("Generate a strong password automatically? (y/n): ").strip().lower()
    if choice == "y":
        password = generate_password()
        print(f"Generated password: {password}")
    else:
        password = getpass.getpass("Enter password: ")

    encrypted = fernet.encrypt(password.encode())

    conn = sqlite3.connect(DB_NAME)
    conn.execute(
        "INSERT INTO accounts (service, username, encrypted_password) VALUES (?, ?, ?)",
        (service, username, encrypted),
    )
    conn.commit()
    conn.close()
    print("Account saved.\n")


def view_accounts(fernet):
    conn = sqlite3.connect(DB_NAME)
    rows = conn.execute("SELECT id, service, username, encrypted_password FROM accounts").fetchall()
    conn.close()

    if not rows:
        print("No accounts saved yet.\n")
        return

    print("\nSaved accounts:")
    for row in rows:
        acc_id, service, username, encrypted_password = row
        try:
            password = fernet.decrypt(encrypted_password).decode()
        except Exception:
            password = "[Error: could not decrypt - wrong master password?]"
        print(f"  [{acc_id}] {service} | {username} | {password}")
    print()


def delete_account():
    acc_id = input("Enter the ID of the account to delete: ").strip()
    conn = sqlite3.connect(DB_NAME)
    conn.execute("DELETE FROM accounts WHERE id = ?", (acc_id,))
    conn.commit()
    conn.close()
    print("Account deleted (if it existed).\n")


def generate_password(length=14):
    chars = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
    return "".join(secrets.choice(chars) for _ in range(length))


# ---------- Main menu ----------
def main():
    init_db()
    salt = get_or_create_salt()

    print("=== Password Manager ===")
    master_password = getpass.getpass("Enter your master password: ")
    key = derive_key(master_password, salt)
    fernet = Fernet(key)

    while True:
        print("1. Add account")
        print("2. View saved accounts")
        print("3. Generate a strong password")
        print("4. Delete an account")
        print("5. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_account(fernet)
        elif choice == "2":
            view_accounts(fernet)
        elif choice == "3":
            print(f"Generated password: {generate_password()}\n")
        elif choice == "4":
            delete_account()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.\n")


if __name__ == "__main__":
    main()
