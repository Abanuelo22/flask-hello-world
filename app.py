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
            CREATE TABLE IF NOT EXISTS Basketball (
                First varchar(255),
                Last varchar(255),
                City varchar(255),
                Name varchar(255),
                Number int
            );
            """
        )

        conn.commit()
        return "Basketball Table Created"

    except Exception as error:
        if conn is not None:
            conn.rollback()

        return f"Error creating Basketball table: {error}"

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
            INSERT INTO Basketball (First, Last, City, Name, Number)
            VALUES
                ('Jayson', 'Tatum', 'Boston', 'Celtics', 0),
                ('Stephen', 'Curry', 'San Francisco', 'Warriors', 30),
                ('Nikola', 'Jokic', 'Denver', 'Nuggets', 15),
                ('Kawhi', 'Leonard', 'Los Angeles', 'Clippers', 2),
                ('Alex', 'Banuelos', 'CU Boulder', 'JGT Finance', 3308);
            """
        )

        conn.commit()
        return "Basketball Table Populated"

    except Exception as error:
        if conn is not None:
            conn.rollback()

        return f"Error populating Basketball table: {error}"

    finally:
        if cursor is not None:
            cursor.close()

        if conn is not None:
            conn.close()


@app.route("/db_select")
def db_select():
    conn = None
    cursor = None

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Basketball;")
        records = cursor.fetchall()

        html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Basketball Table</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 40px;
                }

                table {
                    border-collapse: collapse;
                    width: 100%;
                    max-width: 900px;
                }

                th,
                td {
                    border: 1px solid black;
                    padding: 10px;
                    text-align: left;
                }

                th {
                    background-color: #eeeeee;
                }
            </style>
        </head>
        <body>
            <h1>Basketball Table</h1>
            <table>
                <tr>
                    <th>First</th>
                    <th>Last</th>
                    <th>City</th>
                    <th>Name</th>
                    <th>Number</th>
                </tr>
        """

        for row in records:
            html += "<tr>"

            for value in row:
                html += f"<td>{value}</td>"

            html += "</tr>"

        html += """
            </table>
        </body>
        </html>
        """

        return html

    except Exception as error:
        return f"Error selecting Basketball records: {error}"

    finally:
        if cursor is not None:
            cursor.close()

        if conn is not None:
            conn.close()


@app.route("/db_drop")
def db_drop():
    conn = None
    cursor = None

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        cursor.execute("DROP TABLE IF EXISTS Basketball;")

        conn.commit()
        return "Basketball Table Dropped"

    except Exception as error:
        if conn is not None:
            conn.rollback()

        return f"Error dropping Basketball table: {error}"

    finally:
        if cursor is not None:
            cursor.close()

        if conn is not None:
            conn.close()


if __name__ == "__main__":
    app.run(debug=True)