import os

import psycopg2
from flask import Flask

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")


@app.route("/")
def index():
    return "Hello World from Alex Banuelos in 3308"


@app.route("/db_test")
def db_test():
    conn = None

    try:
        conn = psycopg2.connect(DATABASE_URL)
        return "Database connection successful"
    except Exception as error:
        return f"Database connection failed: {error}"
    finally:
        if conn is not None:
            conn.close()


@app.route("/db_create")
def db_create():
    conn = None
    cursor = None

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS students (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL
            );
            """
        )

        conn.commit()
        return "Students table created successfully"

    except Exception as error:
        if conn is not None:
            conn.rollback()

        return f"Error creating table: {error}"

    finally:
        if cursor is not None:
            cursor.close()

        if conn is not None:
            conn.close()

@app.route("/db_insert")
def db_insert():
    conn = None
    cursor = None

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO students (name)
            VALUES (%s);
            """,
            ("Alex Banuelos",)
        )

        conn.commit()
        return "Student inserted successfully"

    except Exception as error:
        if conn is not None:
            conn.rollback()

        return f"Error inserting student: {error}"

    finally:
        if cursor is not None:
            cursor.close()

        if conn is not None:
            conn.close()


if __name__ == "__main__":
    app.run(debug=True)