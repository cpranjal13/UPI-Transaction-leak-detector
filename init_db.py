import os
import sqlite3
from dotenv import load_dotenv
from db import get_db_connection, is_postgres_available, SQLITE_DB_PATH, DB_HOST, DB_USER, DB_PASS, DB_NAME

load_dotenv()

def init_database():
    if is_postgres_available():
        print(f"PostgreSQL detected on {DB_HOST}. Initializing PostgreSQL database...")
        try:
            import psycopg2
            from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

            conn = psycopg2.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASS,
                database="postgres"
            )
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cur = conn.cursor()
            
            cur.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{DB_NAME}'")
            exists = cur.fetchone()
            
            if not exists:
                print(f"Database '{DB_NAME}' does not exist. Creating...")
                cur.execute(f"CREATE DATABASE {DB_NAME}")
                print(f"Database '{DB_NAME}' created successfully.")
            else:
                print(f"Database '{DB_NAME}' already exists.")
                
            cur.close()
            conn.close()
            
            conn = psycopg2.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASS,
                database=DB_NAME
            )
            cur = conn.cursor()
            
            print("Creating PostgreSQL tables...")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(80) UNIQUE NOT NULL,
                    password_hash VARCHAR(128) NOT NULL,
                    monthly_budget DECIMAL(10, 2) DEFAULT 0.00
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS bank_accounts (
                    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    bank_name VARCHAR(100) NOT NULL,
                    account_no VARCHAR(100) NOT NULL,
                    current_balance DECIMAL(15, 2) NOT NULL,
                    last_updated DATE NOT NULL,
                    PRIMARY KEY (user_id, bank_name, account_no)
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    amount DECIMAL(10, 2) NOT NULL,
                    date DATE NOT NULL,
                    merchant VARCHAR(255) NOT NULL,
                    category VARCHAR(100) NOT NULL,
                    bank_name VARCHAR(100) DEFAULT 'Generic',
                    account_no VARCHAR(100) DEFAULT 'Unknown'
                );
            """)
            conn.commit()
            cur.close()
            conn.close()
            print("PostgreSQL schema initialized successfully!")
            return
        except Exception as e:
            print("PostgreSQL initialization error:", e)
            print("Falling back to initializing SQLite database...")

    # SQLite initialization
    print(f"Initializing SQLite database at: {SQLITE_DB_PATH}")
    conn = get_db_connection()
    conn.close()
    print("SQLite database schema initialized successfully!")

if __name__ == "__main__":
    init_database()
