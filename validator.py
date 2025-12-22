import sqlite3
import requests

DB_PROXIES = "proxies.db"
DB_ITEMS = "valid_items.db"

# --- Proxy DB ---
conn_proxy = sqlite3.connect(DB_PROXIES, check_same_thread=False)
cur_proxy = conn_proxy.cursor()
cur_proxy.execute("CREATE TABLE IF NOT EXISTS proxies (id INTEGER PRIMARY KEY AUTOINCREMENT, proxy TEXT)")
conn_proxy.commit()

def add_proxy(proxy):
    cur_proxy.execute("INSERT INTO proxies(proxy) VALUES (?)", (proxy,))
    conn_proxy.commit()

def list_proxies():
    return cur_proxy.execute("SELECT id, proxy FROM proxies").fetchall()

def remove_proxy(arg):
    if arg == "all":
        cur_proxy.execute("DELETE FROM proxies")
    else:
        cur_proxy.execute("DELETE FROM proxies WHERE id = ?", (arg,))
    conn_proxy.commit()

def proxy_alive(proxy):
    try:
        r = requests.get(
            "https://httpbin.org/ip",
            proxies={"http": f"http://{proxy}", "https": f"http://{proxy}"},
            timeout=7
        )
        return r.status_code == 200
    except:
        return False

def get_alive_proxy():
    for _, p in list_proxies():
        if proxy_alive(p):
            return p
    return None

# --- Items DB ---
conn_item = sqlite3.connect(DB_ITEMS, check_same_thread=False)
cur_item = conn_item.cursor()
cur_item.execute("CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY AUTOINCREMENT, item TEXT)")
conn_item.commit()

def add_item(item):
    cur_item.execute("INSERT INTO items(item) VALUES (?)", (item,))
    conn_item.commit()

def list_items():
    return cur_item.execute("SELECT id, item FROM items").fetchall()

def remove_item(arg):
    if arg == "all":
        cur_item.execute("DELETE FROM items")
    else:
        cur_item.execute("DELETE FROM items WHERE id = ?", (arg,))
    conn_item.commit()

def item_alive(item):
    proxy = get_alive_proxy()
    try:
        if item.startswith("http://") or item.startswith("https://"):
            if proxy:
                r = requests.get(item, proxies={"http": f"http://{proxy}", "https": f"http://{proxy}"}, timeout=7)
            else:
                r = requests.get(item, timeout=7)
            return r.status_code == 200
        # Any string (CC, token, etc.) → assumed valid
        return True
    except:
        return False

def gate_check():
    items = list_items()
    if not items:
        return False, "No items saved"
    for _, i in items:
        if item_alive(i):
            return True, f"Valid → {i}"
    return False, "No valid items found"