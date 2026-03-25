import os
import time
import psycopg2
from flask import Flask


app = Flask(__name__)

DB_HOST = os.getenv("POSTGRES_HOST", "postgres")
DB_PORT = int(os.getenv("POSTGRES_PORT", "5432"))
DB_NAME = os.getenv("POSTGRES_DB", "app_db")
DB_USER = os.getenv("POSTGRES_USER", "app_user")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "")


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
            return conn
        except Exception as exc:
            print(f"Attempt {attempt}/{max_attempts}: DB not ready yet: {exc}")
            time.sleep(delay)
    raise RuntimeError("Could not connect to PostgreSQL")


@app.route("/")
def index():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT users.name, phones.phone
                FROM users
                JOIN phones ON phones.user_id = users.id
                ORDER BY users.id
                LIMIT 100
            """)
            rows = cur.fetchall()
    finally:
        conn.close()

    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <title>Users and Phones</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 40px;
                background: #f7f7f7;
            }
            h1 {
                color: #333;
            }
            table {
                border-collapse: collapse;
                width: 100%;
                background: white;
            }
            th, td {
                border: 1px solid #ccc;
                padding: 10px;
                text-align: left;
            }
            th {
                background: #eee;
            }
        </style>
    </head>
    <body>
        <h1>Users and Phones</h1>
        <table>
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Phone</th>
                </tr>
            </thead>
            <tbody>
    """

    for name, phone in rows:
        html += f"<tr><td>{name}</td><td>{phone}</td></tr>"

    html += """
            </tbody>
        </table>
    </body>
    </html>
    """

    return html


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
