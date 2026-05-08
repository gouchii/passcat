import sqlite3
import os
from cryptography.fernet import Fernet

DB_FILE = "passwords.db"
KEY_FILE = "secret.key"


def _get_encryption_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
    else:
        with open(KEY_FILE, "rb") as f:
            key = f.read()
    return key



cipher_suite = Fernet(_get_encryption_key())


def _init_db():
    """Creates the SQLite database and table if they do not exist."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS passwords
                      (id INTEGER PRIMARY KEY, service TEXT, username TEXT, encrypted_password BLOB)""")
    conn.commit()
    conn.close()


def save_password(service:str, username:str, password:str):
    _init_db()

    encrypted_pwd = cipher_suite.encrypt(password.encode("utf-8"))

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO passwords (service, username, encrypted_password) VALUES (?, ?, ?)",
        (service, username, encrypted_pwd),
    )
    conn.commit()
    conn.close()


def retrieve_passwords()->list:
    _init_db()
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT service, username, encrypted_password FROM passwords")
    rows = cursor.fetchall()
    conn.close()

    results = []
    for service, username, enc_pwd in rows:
        try:
            decrypted_pwd = cipher_suite.decrypt(enc_pwd).decode("utf-8")
            results.append(
                {"service": service, "username": username, "password": decrypted_pwd}
            )
        except Exception as e:
            results.append(
                {
                    "service": service,
                    "username": username,
                    "password": f"ERROR_DECRYPTING {e}",
                }
            )

    return results
