import sqlite3
import random
import string
from datetime import datetime, timedelta

DB_KEYS = "keys.db"
conn = sqlite3.connect(DB_KEYS, check_same_thread=False)
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS keys (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key TEXT UNIQUE,
    duration TEXT,
    used_by INTEGER,
    expires_at TEXT
)""")
conn.commit()

def generate_key(duration):
    """duration: 1d, 10d, 30d, 1m, 6m"""
    key = "samcc_" + "".join(random.choices(string.ascii_letters + string.digits, k=8))
    cur.execute("INSERT INTO keys(key, duration, used_by, expires_at) VALUES (?, ?, ?, ?)",
                (key, duration, None, None))
    conn.commit()
    return key

def redeem_key(user_id, key):
    cur.execute("SELECT duration, used_by FROM keys WHERE key = ?", (key,))
    row = cur.fetchone()
    if not row:
        return False, "Invalid key"
    duration, used_by = row
    if used_by:
        return False, "Key already used"

    # calculate expiration
    now = datetime.utcnow()
    if duration.endswith("d"):
        days = int(duration[:-1])
    elif duration.endswith("m"):
        days = int(duration[:-1]) * 30
    else:
        return False, "Invalid duration"
    expires_at = now + timedelta(days=days)
    cur.execute("UPDATE keys SET used_by = ?, expires_at = ? WHERE key = ?", (user_id, expires_at.isoformat(), key))
    conn.commit()
    return True, "Premium activated"