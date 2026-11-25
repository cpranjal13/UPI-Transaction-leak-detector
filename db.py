import os
import sqlite3
import socket
from datetime import datetime, date
from dotenv import load_dotenv

load_dotenv()

# Database configuration
DB_TYPE = os.getenv("DB_TYPE", "auto")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 5432))
DB_NAME = os.getenv("DB_NAME", "upitracker")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "root")

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SQLITE_DB_PATH = os.path.join(BASE_DIR, "upitracker.db")

class DictRow(dict):
    """Dictionary that also allows index-based access, attribute access, and .get()."""
    def __getitem__(self, key):
        if isinstance(key, int):
            return list(self.values())[key]
        return super().__getitem__(key)

    def __getattr__(self, name):
        if name in self:
            return self[name]
        raise AttributeError(f"'DictRow' object has no attribute '{name}'")

class SQLiteCursorWrapper:
    def __init__(self, cursor):
        self._cursor = cursor
        self._rows = []
        self._row_idx = 0

    def execute(self, query, params=None):
        sqlite_query = query.replace('%s', '?')
        if params is None:
            self._cursor.execute(sqlite_query)
        else:
            converted_params = []
            for p in params:
                if isinstance(p, (datetime, date)):
                    converted_params.append(p.strftime('%Y-%m-%d'))
                else:
                    converted_params.append(p)
            self._cursor.execute(sqlite_query, tuple(converted_params))
        
        # Buffer rows if statement returns columns (SELECT, RETURNING)
        # to ensure SQLite doesn't complain about statements in progress during commit
        if self._cursor.description:
            self._rows = self._cursor.fetchall()
            self._row_idx = 0
        else:
            self._rows = []
            self._row_idx = 0
        return self

    def fetchone(self):
        if self._row_idx < len(self._rows):
            row = self._rows[self._row_idx]
            self._row_idx += 1
            return self._make_dict_row(row)
        return None

    def fetchall(self):
        remaining = self._rows[self._row_idx:]
        self._row_idx = len(self._rows)
        return [self._make_dict_row(r) for r in remaining]

    def _make_dict_row(self, row):
        if not self._cursor.description:
            return row
        d = {}
        for idx, col in enumerate(self._cursor.description):
            col_name = col[0]
            val = row[idx]
            # Convert decimal/float fields so Jinja2 and math operations work consistently
            if col_name in ('amount', 'current_balance', 'monthly_budget') and val is not None:
                try:
                    val = float(val)
                except (ValueError, TypeError):
                    pass
            d[col_name] = val
        return DictRow(d)

    def close(self):
        self._cursor.close()

    @property
    def rowcount(self):
        return self._cursor.rowcount

class SQLiteConnectionWrapper:
    def __init__(self, conn):
        self._conn = conn

    def cursor(self, cursor_factory=None):
        return SQLiteCursorWrapper(self._conn.cursor())

    def commit(self):
        self._conn.commit()

    def rollback(self):
        self._conn.rollback()

    def close(self):
        self._conn.close()

def is_postgres_available():
    """Quick check if PostgreSQL port is open."""
    if DB_TYPE.lower() == 'sqlite':
        return False
    if DB_TYPE.lower() in ('postgres', 'postgresql'):
        return True
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((DB_HOST, DB_PORT))
        sock.close()
        return result == 0
    except Exception:
        return False

def init_sqlite_schema(conn):
    """Initializes SQLite database tables."""
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            monthly_budget REAL DEFAULT 0.00
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS bank_accounts (
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            bank_name TEXT NOT NULL,
            account_no TEXT NOT NULL,
            current_balance REAL NOT NULL,
            last_updated TEXT NOT NULL,
            PRIMARY KEY (user_id, bank_name, account_no)
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            amount REAL NOT NULL,
            date TEXT NOT NULL,
            merchant TEXT NOT NULL,
            category TEXT NOT NULL,
            bank_name TEXT DEFAULT 'Generic',
            account_no TEXT DEFAULT 'Unknown'
        );
    """)
    conn.commit()
    cur.close()

def get_db_connection():
    """Returns database connection (PostgreSQL if available, otherwise SQLite)."""
    if is_postgres_available():
        try:
            import psycopg2
            return psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASS
            )
        except Exception as e:
            print(f"[DB] PostgreSQL connection failed ({e}). Falling back to SQLite.")
            
    conn = sqlite3.connect(SQLITE_DB_PATH, check_same_thread=False)
    conn.execute("PRAGMA foreign_keys = ON")
    init_sqlite_schema(conn)
    return SQLiteConnectionWrapper(conn)
