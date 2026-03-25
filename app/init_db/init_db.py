import os
import random
import time

import psycopg2


DB_HOST = os.getenv("POSTGRES_HOST", "postgres")
DB_PORT = int(os.getenv("POSTGRES_PORT", "5432"))
DB_NAME = os.getenv("POSTGRES_DB", "app_db")
DB_USER = os.getenv("POSTGRES_USER", "app_user")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "")


FIRST_NAMES = [
    "Ivan", "Alex", "Nikita", "Sergey", "Pavel",
    "Anna", "Maria", "Elena", "Olga", "Daria",
    "Maxim", "Artem", "Dmitry", "Kirill", "Andrey"
]


def random_phone() -> str:
    return f"+79{random.randint(10,99)}{random.randint(1000000,9999999)}"


def get_connection(max_attempts: int = 20, delay: int = 3):
    for attempt in range(1, max_attempts + 1):
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
            )
            print("Connected to PostgreSQL")
            return conn
        except Exception as exc:
            print(f"Attempt {attempt}/{max_attempts}: cannot connect yet: {exc}")
            time.sleep(delay)
    raise RuntimeError("Could not connect to PostgreSQL after several attempts")


def create_tables(cur):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS phones (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            phone TEXT NOT NULL
        );
    """)


def seed_data(cur, count: int = 100):
    cur.execute("SELECT COUNT(*) FROM users;")
    existing_users = cur.fetchone()[0]

    if existing_users >= count:
        print(f"Database already contains {existing_users} users, skipping seed")
        return

    for _ in range(count):
        name = random.choice(FIRST_NAMES)
        cur.execute(
            "INSERT INTO users (name) VALUES (%s) RETURNING id;",
            (name,)
        )
        user_id = cur.fetchone()[0]

        cur.execute(
            "INSERT INTO phones (user_id, phone) VALUES (%s, %s);",
            (user_id, random_phone())
        )

    print(f"Inserted {count} users and phones")


def main():
    conn = get_connection()
    conn.autocommit = False

    try:
        with conn.cursor() as cur:
            create_tables(cur)
            seed_data(cur, count=100)
        conn.commit()
        print("Database initialization completed successfully")
    except Exception as exc:
        conn.rollback()
        print(f"Database initialization failed: {exc}")
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
