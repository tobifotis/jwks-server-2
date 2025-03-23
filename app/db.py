import sqlite3
from cryptography.hazmat.primitives import serialization

DB_NAME = "totally_not_my_privateKeys.db"


def initialize_db():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS keys (
            kid INTEGER PRIMARY KEY AUTOINCREMENT,
            key BLOB NOT NULL,
            exp INTEGER NOT NULL
        )
    ''')
    connection.commit()
    connection.close()


def save_private_key(private_key, exp):
    pem_key = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO keys (key, exp) VALUES (?, ?)", (pem_key, exp))
    connection.commit()
    connection.close()


def fetch_key(expired=False):
    import datetime
    from cryptography.hazmat.primitives.serialization \
        import load_pem_private_key

    now = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    if expired:
        cursor.execute(
            "SELECT kid, key FROM keys WHERE exp < ? "
            "ORDER BY exp DESC LIMIT 1",
            (now,)
        )

    else:
        cursor.execute(
            "SELECT kid, key FROM keys WHERE exp > ? ORDER BY exp ASC LIMIT 1",
            (now,)
        )

    row = cursor.fetchone()
    connection.close()

    if row:
        return row[0], load_pem_private_key(row[1], password=None)
    return None, None
